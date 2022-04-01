# 실습 1: Amazon EKS 환경 구축

## 과제 1: 배스천 호스트에 연결

## 과제 2: Amazon EKS 클러스터 및 관리형 노드 그룹 배포

### kubectl 설치

```bash
sudo curl --location -o /usr/local/bin/kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.21.2/2021-07-05/bin/linux/amd64/kubectl # kubectl 유틸리티 다운로드

sudo chmod +x /usr/local/bin/kubectl # kubectl을 실행파일로 만들기
kubectl version --short --client # 버전확인
```

### eksctl 설치

```bash
curl --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp # 다운로드 및 압축풀기
sudo mv -v /tmp/eksctl /usr/local/bin # 폴더 이동
eksctl version # 버전확인
```

- /user/local/bin 폴더로 이동하면 PATH 구성이 되기때문에, eksctl 명령어를 사용할 수 있음

### 현재 리전 환경변수로 설정

```bash
export AWS_REGION=$(curl --silent http://169.254.169.254/latest/meta-data/placement/region) && echo $AWS_REGION
```

### 3개 노드로 구성된 관리형 노드그룹이 있는 EKS 클러스터를 배포합니다.

```bash
eksctl create cluster \           # EKS 클러스터 배포
--name dev-cluster \              # 클러스터 이름지정
--nodegroup-name dev-nodes \      # 노드그룹 이름
--node-type t3.small \            # 노드에 사용되는 인스턴스 유형
--nodes 3 \                       # AutoScaling 정의 중에 배포되는 노드 수
--nodes-min 1 \                   # AutoScaling 최소 노드 수
--nodes-max 4 \                   # AutoScaling 최대 노드 수
--managed \                       # EKS 관리형 노드 그룹 생성
--region ${AWS_REGION}            # EKS 클러스터 및 노드 그룹을 배포할 AWS 리전을 지정 ( default: us-west-2 )
```

- eksctl create cluster 명령은 CloudFormation을 활용해서 EKS의 컨트롤 플레인 클러스터에 필요한 리소스를 만듦.

### 생성된 노드 확인하기

```bash
kubectl get nodes
```

## 과제 3: 샘플 애플리케이션 배포 및 구성

### 홈 디렉터리로 전환

```bash
cd ~
```

### S3에서 샘플 애플리케이션 복사해오기

```bash
aws s3 cp s3://aws-tc-largeobjects/ILT-TF-200-COREKS-10-EN/lab-1/ecsdemo-crystal/ ~/ecsdemo-crystal/ --recursive
aws s3 cp s3://aws-tc-largeobjects/ILT-TF-200-COREKS-10-EN/lab-1/ecsdemo-frontend/ ~/ecsdemo-frontend/ --recursive
aws s3 cp s3://aws-tc-largeobjects/ILT-TF-200-COREKS-10-EN/lab-1/ecsdemo-nodejs/ ~/ecsdemo-nodejs/ --recursive
```

### Node.js API 서버 배포하기

```bash
cd ~/ecsdemo-nodejs
kubectl apply -f kubernetes/deployment.yaml # deployment.yaml을 이용해 Node.js API 서버 배포하기
kubectl apply -f kubernetes/service.yaml    # service.yaml을 이용해 서비스 연결하기
kubectl get deployment ecsdemo-nodejs       # 배포 진행사항 확인하기
```

### crystal 배포하기

```bash
cd ~/ecsdemo-crystal
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl get deployment ecsdemo-crystal
```

### frontend 배포하기

```bash
cd ~/ecsdemo-frontend
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl get deployment ecsdemo-frontend
```

### default 네임스페이스의 모든 Kubernetes Deployment를 나열

```bash
kubectl get deployments
```

### External IP 확인하기

```bash
kubectl get service ecsdemo-frontend -o wide

# NAME               TYPE           CLUSTER-IP      EXTERNAL-IP                                                               PORT(S)        AGE   SELECTOR
# ecsdemo-frontend   LoadBalancer   10.100.14.212   a986519dd362044bd95c8f9eb60f9b3f-1860343235.us-west-2.elb.amazonaws.com   80:31518/TCP   85s   app=ecsdemo-frontend
```

- EXTERNAL-IP ( HTTP )

## 과제 4: 포드 탐색 및 애플리케이션 설치

### default 네임스페이스의 포드 확인하기

```bash
kubectl get pods -n default
export MY_POD_NAME=$(kubectl get pods -n default -o jsonpath='{.items[0].metadata.name}') # 첫번째 포드이름을 환경변수에 저장하기
# ecsdemo-crystal-856c46f686-57hlx


```

### 포드의 세부정보 확인하기

```bash
kubectl -n default describe pod $MY_POD_NAME
```

### 포드의 bash shell에 연결하기

```bash
kubectl exec -it ${MY_POD_NAME} -n default -- /bin/bash
exit # pod에서 연결 해제하기
```

## 과제 5: 애플리케이션 Deloyment 확장

### kubectl scale deployment를 이용하여 replicas 확장하기

```bash
kubectl scale deployment ecsdemo-nodejs --replicas=3
kubectl scale deployment ecsdemo-crystal --replicas=3
```

### kubectl scale deployment를 이용하여 replicas 축소하기

```bash
kubectl scale deployment ecsdemo-nodejs --replicas=2
kubectl scale deployment ecsdemo-crystal --replicas=2
```

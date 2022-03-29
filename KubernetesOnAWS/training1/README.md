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



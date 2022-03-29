# Kubernetes On AWS

## Kubernetes Basic

### Volume

- EmptyDir 임시
- HostPath 로컬
- PersistentVolume 영구

### CSI 드라이버

- Pod -> EFS 탑재대상 -> EFS

### ConfigMap 과 Secret

- ConfigMap: key-value 값으로 저장
- ConfigMap을 불러오는 방법 2가지 ( 환경변수, 볼륨 )
- Secret: Base64 인코딩
- Secret은 보안적으로 좋다

### Namespace

- 하나의 클러스터를 논리적으로 나눠서 사용할 수 있도록 도와줌
- 기본적으로 default이 있음
- kube-public, kube-system이 기본적으로 존재
- 별도의 namespace를 만들거나 default에 저장
- 논리적으로 나눠주게 함
- 권함도 네임스페이스 안에서만 줄 수 있음/ 심지어 CPU량도 조절 가능함

### Deployments와 ReplicaSets

- Deployment : replicaset 롤아웃 ( 변경사항 업데이트 )

### Pod 스케줄링

- 조건자: 규칙은 특정 노드에서 Pod를 스케줄링할 수 있는지 여부를 결정
- 우선순위: 점수는 Pod 배치를 위한 최적의 노드를 결정

### 토폴로지 - Taint와 tolerations

- taint로 제한 tolerations로 허용
- 사용예시: Spot Instance, GPU

### 토폴로지 - Affinity

- [Scheduler](https://kubernetes.io/ko/docs/reference/scheduling/policies/)

### 토폴로지 - DaemonSet

- Pod를 DaemonSet을 통해 배치
- 모니터링용으로 pod를 배치시킬수 있다.

```bash
kubectl api-resources
kubectl apply -f nginx-deployment.yaml

kubectl get all

```

### 관리형 Kubernetes

- 컨트롤플레인: 완전 관리형
- 데이터플레인: 관리형 노드그룹 / Fargate

### 네트워크/스토리지 연동

- VPC CNI ( 네트워트 )
- VPC CNS ( 스토리지 )

### 인증

- 쿠버네티스는 기본적으로 인증없음
- IAM + RBACK이 이미 인증이 연동되어있음

### AWS 플랫폼 연동

- ELB 이용, CloudWatch에서 로그 구성

## 데이터플레인

### 데이터플레인 옵션

- 작업자 노드
- 관리형 노드 그룹
- AWS Fargate

### Fargate

- DemonSets을 지원하지 않음
- Pod안에 모니터링 컨테이너도 두고 이를 이용함

### Fargate 프로파일

- Fargate에 대한 정보를 미리 등록

### 인증 및 권한 부여

### IAM 및 K8s RBAC

- k8s api는 IAM을 RBAC과 연동
- IAM Authenticator

### eksctl

- [eksctl](https://eksctl.io/usage/schema/)

### 클러스터 생성을 위한 선언적 옵션

- AWS CloudFormation
- AWS CDK
- HasiCorp Terraform

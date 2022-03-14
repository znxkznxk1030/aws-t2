# aws t2 교육 필기

## 모듈 0: AWS 기반 아키텍쳐 설계 시작

## 모듈 1: 소개

### 간단한 복습

- 클라우드 설계 지침 -> Well-Architected 프레임워크
- AWS 글로벌 인프라 : 리전 ( Region ), 가용영역 ( AZ : Available Zone )
- 대규모 아키택처 설계

### 아키텍처 측면에서 필요성

- Amazon.com 전자 상거래 도구는 뒤죽박죽 이였음.
- 에플리케이션 및 아키텍처가 적절한 계획없이 구축된것.
- 서비스는 구분 되어야 했음.
- => 도구가 잘 문서화된 일련의 API로 정비되어 Amazon에서 서비스 개발을 위한 표준이 되었음. ( => AWS )

#### 문제 지속

- 여전히 Amazon.com은 신속히 애플리케이션을 구축하는데 어려움

- => 인프라 상에 고가용성,탄력싱 필요함에 따라 클라우드로 발전

#### 클라우드란? AWS란?

- 프로그래밍 가능한 리소스 ( IaC )
- 동적기능

### 클라우드 컴퓨팅의 6가지 장점

1. 자본비용을 가변 비용으로 대체
1. 규모의 경제로 부터 이점
1. 용량 추정 불필요
1. 속도 및 민첩성 개선
1. 중요한 문제에 집중
1. 몇분만에 전 세계에 배포

### Well Architected 프레임 워크 ( WAF )

[Well Architected Framework](https://aws.amazon.com/ko/architecture/well-architected/?nc1=h_ls&ampwa-lens-whitepapers.sort-by=item.additionalFields.sortDate&ampwa-lens-whitepapers.sort-order=desc&wa-lens-whitepapers.sort-by=item.additionalFields.sortDate&wa-lens-whitepapers.sort-order=desc)

- 보안
- 안정성
- 비용최적화
- 성능 효율성
- 운영 우수성
- 지속가능성 ( 새롭게 추가 됨 ) - 환경에 미치는 영향을 최소화 함

#### 보안

- 자격 증명 기반
- 추적 가능성 활성화
- 모든 계층에서의 보안
- 위험 평가 및 완화

#### 비용 최적화

- 효율성 측정
- 불필요한 비용 제거
- 관리형 서비스 사용을 고려

#### 성능 효율성

- 요율적인 리소스 선택, 수요 변화에 맞추기
- 고급 기술을 대중화 ( 예: 머신러닝 도입할때, 있는 기술 가져다가 쓰자 )
- Mechanical sympathy ( 개발자, 아키텍쳐 모두 인프라에 대한 이해가 있어야 한다. )

### 글로벌 인프라

![global infra](./figures/region.png)

#### AWS 데이터 센터

- 보통 단일 데이터 센터에서 수반개의 서버를 운영
- 모든 데이터 센터는 "콜드 연결"이 아니라 온라인으로 연결됨
- AWS 사용자 정의 네트워크 장비
  - 다양한 ODM () 사용
  - 사용자 지정 네트워크 프로토콜 스택

### 가용 영역

- 각 가용영역은 하나이상의 데이터 센터

### 리전

- 두 개 이상의 가용영역으로 이루어져 있음 ( 서울은 4개 )
- 리전간 데이터 복제를 활성화
- AWS 백본 네트워크 인프라 사용 ( 별도의 네트워크 인프라 사용 | 인터넷보다 훨씬 빠름 )

[AWS | global infrastructure](https://aws.amazon.com/ko/about-aws/global-infrastructure/)

- Data Center와 POP( Points of Presence, Edge Location ) 와는 다른 장비이다.
- POP는 CloudFront, Route 53 같은 서비스 제공
- 각 리전별로 제공되는 서비스는 각기 다르다

#### 아키텍쳐용 리전

- 데이터 주권 및 규정 준수
- 사용자와 데이터간 근접성
- 서비스 및 기능 가용성 ( 내가 필요한 서비스가 그 리전에 없을수도 있기 때문에 )
- 비용 효율성

## 모듈 2: 가장 간단한 아키텍쳐

![S3](./figures/s3.png)

### Amazon S3

- 객체 수준 스토리지
- 99.999999999% 내구성을 제공
- 이벤트 트리거 ( 생성/삭제등 이벤트에 대해서 람다로 트리거 가능 )

### 스토리지의 종류

#### File Storage

- NAS같은 것들
- Network: LAN
- AWS: EFS, FSx for windows

#### Block Storage

- Network : Local I/O
- AWS: EBS, Instance Store

#### Object Storage

- google box, drive 같은 것들
- Network: internet
- AWS: S3

### S3 사용 사례 1 - 정적 웹 콘텐츠와 미디어 저장 및 배포


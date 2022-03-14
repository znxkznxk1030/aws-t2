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
  - 다양한 ODM (Original Design Manufacturer) 사용 ( 일반적인 장비가 아닌 별도로 디자인된 장비를 사용 )
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

![module - 2](./figures/s3.png)

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
- 오브젝트 스토리지 특성상 올라가 있는 장소에서 직접 수정 불가능

### S3 사용 사례 1 - 정적 웹 콘텐츠와 미디어 저장 및 배포

#### 엑세스 제어 - 일반

- 비공개 : 소유자에게만 접근 허용
- 공개 : 다른 사람에게도 접근 허용
- 제한된 액세스: 사용자를 선별적으로 접근 허용 가능

#### 액세스 제어 - 버킷 정책

- IAM 서비스에 의해 정해진다
- JSON으로 표현 ( AWS Policy Generator )
- 때로는 도큐먼트가 관리가 어려울 수 있음

#### 액세스 포인트

- 엔드포인트를 사용하여 데이터에 액세스 하는 방법을 설명하는 전용 액세스 정책을 포함하는 고유한 호스트 이름
- 액세스 포인트에 따라 액세스 정책을 적용
- 다음을 지원
  - 단일사용자
  - 애플리케이션
  - 사용자들의 그룹 또는 애플리케이션

### S3 사용 사례 2 - 전체 정적 웹사이트 호스팅

#### 버전관리

- 실수로 삭제/ 오버라이트 된 경우데 롤백 가능하도록 버전 관리 제공
- 데이터 보존 또는 보호를 위해 S3 객체 잠금 사용 | 사용자의 실수/고의적으로 한번 올려진 데이터를 삭제하지 못하게 하는 기능

### S3 사용 사례 3 - 연산 및 대규모 분석용 데이터 스토어 ( Data Lake )

- 금융 거래 분석
- 클릭스트림 분석
- 미디어 트랜스코딩

### S3 사용 사례 4 - 백업도구

1. 회사 데이터 백업 데이터 저장
1. EC2의 백업 snapshot 저장

### S3로 데이터를 이동

- 버킷은 100개 객체수는 무제한
- 모든 파일 유형 지원
- API을 통한 작업
  1. 콘솔
  1. CLI
  1. SDK

### S3 멀티파트 업로드 지원

- 병렬로 올려서 빠르고
- 한개의 네트워크에서 세션 오류가 나더라도 복귀하기 쉬움
- 쪼개진 데이터는 버킷에서 하나로 합쳐진다

### S3 Transfer Acceleration

1. 일반 인터넷으로 전송
2. 엣지 로케이션까지 인터넷으로 옮기고, 내부에선 Amazon 네트워크를 통해 Amazon S3로 옮김 ( Amazon 내부 네트워크 속도는 매우 빠르다 )

- [Amazon S3 Transfer Acceleration 속도비교](http://s3-accelerate-speedtest.s3-accelerate.amazonaws.com/en/accelerate-speed-comparsion.html)

![Amazon S3 Transfer Acceleration Comparison](./figures/speed-comparison.png)

- 514배 빠르다.

![Amazon S3 Transfer Acceleration Comparison 2](./figures/speed-comparison-2.png)

- 서울은 인터넷이 6% 더 빠르다.

### S3는 언제 사용해야 합니까?

#### + 모범 사용 사례

- 한번 쓰고 여러번 읽어야 하는 경우
- 데이터 액세스가 일시적으로 급증하는 경우
- 사용자가 매우 많고 콘텐츠양이 다양
- 데이터 세트가 계속 증가

#### - 불량 사용 사례

- 블록 스토리지 요구사항
- 자주 바뀌는 데이터
- 장기 아카이브 스토리지

### Amazon S3 Glacier

- 비용 : 신속 검색, 표준 검색

#### S3 스토리지 클래스

- Standard: 자주 액세스 하는 데이터
- Standard IA: 수명이 길고 자주 액세스 하지 않는 데이터
- One Zone IA : 자주 액세스하지 않지만, 빠른 액세스가 필요한 데이터, 하나의 가용영역에만 저장하기 때문에 가용성은 좀 떨어 질 수 있다.
- Glacier/Deep Archive (Deep Archive 사용하면 검색시 12시간에서 48시간 걸린다)

#### Amazon S3 인텔리전트 티어링

- 스토리지의 두 액세스 티어 사이에서 자동으로 객체 이동

### 수명 주기 정책

- 생성 후 기간을 기준으로 객체를 삭제 또는 이동 할 수 있습니다.

## 모듈 3 : 컴퓨터 계층 추가

- 적은 수의 일관된 사용자가 사용할 애플리케이션을 실행

![module - 3](./figures/ec2.png)

### 모듈 개요

- EC2
- 인스턴스 유형 및 패밀리
- EBS 볼륨
- 규정 준수 옵션

### Amazon 머신 이미지 (AMI)를 사용하여 Amazon EC2 인스턴스 시작

1. Pre-Built ( by Amazon ) 또는 퍼블릭 커뮤니티 AMI
2. AMI + Instance Type (F.G.S | Family, Generation, Size | ex: t2.large)
3. Configure Instance : 사용자 데이터, VPC | Subnet, 스팟 인스턴스, ENI, Public IP <-> EIP (Elastic IP| 5개/Region), 배치그룹, IAM Role: Instance Profile
4. Add Storage : EBS/Instance Storage ( 인스턴스 스토어는 모든 인스턴스 타입에서 지원 되지는 않는다. ex: t2 - X, c5d.large, c5d.xlarge)
5. Configuare Security Group
6. Key Pair : Pub/Pri
7. Launch Instance

- 런치된 인스턴스(Web/WAS)를 가지고 AMI로 만듬 ( 기본적으로 private 한 이미지 )

- metadata: 인스턴스를 설명하는 데이터: 실행중인 인스턴스를 구성 또는 관리

```bash
curl http://169.254.169.254/lastest/meta-data/instance-id
```

- t Family를 사용해서 인스턴스를 만들면 성능이 좋아 보다 저렴하다.

### EBS vs Instance Store( Storage )

### AMI는 어떠한 도움을 줍니까?

- 반복성
- 재사용성
- 복구성
- Marketplace 솔루션
- 백업

### 사용자 데이터를 사용하여 EC2 인스턴스 시작

사용자 AMI -> ( 아래 명령어 ) -> EC2 인스턴스 실행

```bash
yum update -y
service httpd start
chkconfig httpd on
```

### 인스턴스 메타데이터를 사용하여 EC2 인스턴스에 대한 정보 가져오기

사용자 AMI -> ( 아래 명령어 ) -> EC2 인스턴스 실행

```bash
!bin/bash
yum update -y
host = $(curl http://169.254.169.254/lastest/meta-data/instance-id)
```

### EBS ( Elastic Block Storage )는 어떤 문제를 해결합니까?

- 애플리케이션에는 블록수준 스토리지가 필요
- 인스턴스 스토어는 휘발성
- 종료후에도 데이터가 지속
- 데이터 볼륨을 백업
- 유의사항: 동일한 인스턴스에 여러 Amazon EBS볼륨이 있을 수 있지만 각 볼륨은 한번에 하나의 인스턴스에만 연결 할 수 있음

### EBS 볼륨 유형 ( 부트 볼륨이 될 수 없음 )

- 처리량 최적화 HDD : 자주 액세스
- 콜드 HDD : 자주 액세스 X

### 공유 파일 시스템 - 여러 인스턴스가 동일한 스토리지를 사용해야 하는 경우 어떻게 해야 합니까?

- EFS/FSx 가 적합
- EBS는 하나의 인스턴스에만 연결
- S3도 옵션이지만 이상적이지 않음

### Amazon FSx

- Windows/Lustre 워크로드

### EC2 인스턴스 유형

- 효율적인 인스턴스 사용률
- 불필요한 비용을 절감

#### 범용 - t, m

#### 컴퓨팅 최적화 - c

#### 메모리 최적화 - r

#### 엑셀러레이트 - p

#### 스토리지 최적화 - h

#### 인텔 제온 CPU - 최신식 제온 확장형 프로세서 사용하고 있다.

### EC2 - 비용

- 온디맨드 인스턴스
- 예약 인스턴스
- Saving Plans
- 스팟 인스턴스

- on-demand가 제일 비싸고 spot instance가 제일 싸다 ( 최대 90% 저렴 )
- Reserved Instance, Saving Plans를 이용하면 on-demand 보단 더 싸게 이용 할수 있다. ( 40 ~ 70% 저렴 )

#### 온디맨드 인스턴스

- 초당 또는 시간당

#### 예약 인스턴스

- 용량에 대한 비용을 미리 지불
- 스탠다드 RI, 컴버터블 RI, 예약 RI
- 3가지 선결제 방법
- 여러 계정 사이에서 공유 가능

#### Savings Plans

- 스탠다드 RI, 컴버터블 RI 에서 확장형
- 예약 인스턴스에서 유연한 기능 제공

#### Spot Instance

- 인스턴스 종료 2분 전에 중단공지 받음

### EC2 전용 옵션

- 전용 인스턴스
- 전용 호스트

### 태그지정 모범사례

- 리소스 태그를 관리하는데 도움이 되는 자동화된 도구를 구현
- 태그는 너무 적게 사용하는 것보다 너무 많이 사용하는 것이 낫습니다
- 수정하기 쉽습니다
- 예: 앱버전, ENV, DNS 이름, 앱 스택 식별자

### EC2 고려사항

### 아키텍쳐 고려사항 1

- Cluster Placement Groups

- Spread Placement Groups

- Partition Placement Groups

![architect](./figures/architect-1.png)

## 모듈 4: 데이터베이스 계층 추가

![module - 4](./figures/database.png)

### 구조화된 데이터 스토리지 비교 및 대조

- 관계형 : sql기반 쿼리, 확장성 수직적
- 비관계형: 문서 수집에 집중, 수평적 확장

### 비관리형 데이터 베이스

- AWS가 관리 하지 않는 데이터 베이스

### RDS의 엔진

- Oracle
- MySql
- MariaDB
- postgreSQL
- MS-SQL
- Aurora ( MySql/ PostgreSQL )

### Amazon RDS 및 Amazon Aurora

- MySql및 Postgre와 호환되는 완전 관리형 데이터 베이스

### Amazon DynamoDB

- 완전 관리형 비관계형 데이터베이스 서비스
- 이벤트 중심 프로그래밍 ( 서버리스 컴퓨팅 )
- 최상의 수평 확장 기능

#### DynamoDB의 글로벌 테이블

- 단일 AWS계정이 소유하고 복제본 테이블로 식별되는 한개이상의 DynamoDB 테이블의 모음.
- 복제본 테이블은 글로벌 테이블의 일부로 기능하는 단일 DynamoDB 테이블
- 리전당 한 개의 복제본 테이블을 가질 수 있음.
- DynamoDB의 Streams라는 기능 사용 ( 변경된 사항이 있으면, 다른 리전으로 복제를 해줌 )

#### DynamoDB 일관성 옵션

- 최종적 일관성 ( = default, 0.5x 읽기, 강력한 일관성에 비해 2배더 읽을 수 있음)
- 강력한 일관성

### RDS 보안제어

- DB 자체에 대한 액세스
- 저장시 암호화
- 전송중 암호화
- 이벤트 알림

### DynamoDB 보안제어

- 정의 가능한 엑세스 권한 : 테이블에서 항목, 심지어 속성까지 모두 관리 가능
- 저장시 암호화
- SSL/TLS
- 고객 관리형 키

### AWS데이터베이스로 데이터 마이그레이션

- on-premise => aws

### AWS Database Migration Service ( DMS )

#### 데이터 마이그레이션이 힘든경우

- 데이터베이스가 너무 큼
- 연결이 너무 느림
- 개인 정보 보호 및 보안 문제

=> AWS Snowball Edge ( Snowball v2 )를 권장 ( Snowball 도 S3)

- Snowball Edge 디바이스를 사용하여 하나이상의 데이터베이스를 마이그레이션을 할수 있습니다
- 멀티 테라바이트 스토리지
- 인터넷 또는 DX 대역폭 사용

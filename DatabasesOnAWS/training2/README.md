# Amazon Aurora 데이터베이스 사용하기

## 작업2: 데이터 및 병렬 쿼리 설정 탐색

```bash
cd ~
mysql -u dbadmin -p -h qdpwgszoilxzjn.cosisna12bf9.us-west-2.rds.amazonaws.com
```

```sql
USE ontimeflights;
SHOW TABLES;
```

```sql
DESCRIBE carriers;
SELECT FORMAT(COUNT(carrierCode), 0) AS 'Number of Carriers' FROM carriers;
```

```sql
DESCRIBE flightdata;
SELECT FORMAT(COUNT(Year), 0) AS 'Number of Flights' FROM flightdata;
```

- 테이블 행수를 표시하는데 5분정도 걸림 ( 3,000만개의 행이 있음 )

### 병렬 쿼리 지원 여부 확인

```sql
SELECT @@aurora_pq_supported;
SELECT @@aurora_pq;
```

#### 병렬쿼리 비활성화

```sql
SET SESSION aurora_pq = 0; -- 비활성화
SET SESSION aurora_pq = 1; -- 활성화
```

### 실행문에 병렬 처리 추천 여부 확인하기

```sql
-- 병렬쿼리를 추천하지 않는 쿼리
EXPLAIN
SELECT
  Origin, Dest, Reporting_Airline,
  AVG(DepDelayMinutes) 'Avg Departure Delay', COUNT(DepDelay) 'Delayed Flights'
FROM flightdata;
```

- Extra에서 NULL이 표시된다면 병렬처리를 추천하지 않는 쿼리

```sql
-- 병렬쿼리를 추천하는 쿼리
EXPLAIN
SELECT
  Origin, Dest, Reporting_Airline,
  AVG(DepDelayMinutes) 'Avg Departure Delay', COUNT(DepDelay) 'Delayed Flights'
FROM flightdata
WHERE DepDelay > 0
AND Origin NOT IN ('TWF', 'SNA', 'ORD');

-- 병렬쿼리를 추천하는 쿼리
EXPLAIN
SELECT
  Origin, Dest, Reporting_Airline,
  AVG(DepDelayMinutes) 'Avg Departure Delay', COUNT(DepDelay) 'Delayed Flights'
FROM flightdata
WHERE DepDelay > 0
AND Origin NOT IN ('TWF', 'SNA', 'ORD')
AND ArrDelayMinutes > DepDelayMinutes;
```

- Extra에서 "Using where; Using parallel query (5 columns, 1 filters, 1 exprs; 0 extra)" 같은 병렬쿼리 추천 메세지 표시

### innoDB 버퍼 풀 출력

```sql
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool%';
```

- | Innodb_buffer_pool_read_requests | 414950934 |

### 병렬쿼리옵션을 끄고 쿼리 처리하기

```sql
SET SESSION aurora_pq = 0;
SET SESSION aurora_pq_force=0;

SELECT AVG(DepDelayMinutes + ArrDelayMinutes) AS "Average Delay"
FROM flightdata
WHERE Distance > 200
AND
OriginCityName NOT IN ('Chicago IL', 'Miami FL');
```

#### Innodb_buffer_pool_read_requests 값 전후 비교하기

- 전: | Innodb_buffer_pool_read_requests | 414950934 |
- 후: | Innodb_buffer_pool_read_requests | 445807673 |
- 총 읽기 요청수 : 445807673 - 414950934 = 30,856,739

### 병렬쿼리옵션을 켜고 쿼리 처리하기

```sql
SET SESSION aurora_pq = 1;
SET SESSION aurora_pq_force=1;

SELECT SQL_NO_CACHE AVG(DepDelayMinutes + ArrDelayMinutes) AS "Average Delay"
FROM flightdata
WHERE Distance > 200
AND
OriginCityName NOT IN ('Chicago IL', 'Miami FL');
```

- 전: | Innodb_buffer_pool_read_requests | 445807673 |
- 후: | Innodb_buffer_pool_read_requests | 454534638 |
- 총 읽기 요청수 : 454534638 - 445807673 = 8,726,965
- 병렬처리를 해서 쿼리를 처리해보니 읽기요청수가 현저히 줄어든것을 알 수 있다.

### 한번 질의한 쿼리는 캐시에 저장되어서 바로 결과를 출력한다.

## 작업 4:

### 인스턴스 크기가 작은곳에서의 성능

- 현재 rdb 서버 인스턴스 : db.r5.large

```sql
SET SESSION aurora_pq=0; -- 병렬쿼리 ON 시킬때는 1로 변경
SET SESSION aurora_pq_force=0; -- 병렬쿼리 ON 시킬때는 1로 변경

SELECT SQL_NO_CACHE
  carriers.carrierName AS 'Carrier',
  flightdata.Origin AS 'Origin Airport',
  flightdata.Dest AS 'Destination Airport',
  AVG(flightdata.ArrDelay) AS 'Average Arrival Delay',
  COUNT(flightdata.ArrDelay) AS 'Number of Delays',
  SUM(flightdata.Cancelled) AS 'Cancelled Flights'
FROM flightdata
LEFT JOIN carriers
ON carriers.carrierCode = flightdata.Reporting_Airline
WHERE flightdata.Distance < 1000
AND carriers.carrierCode IN ("AA", "UA", "DL", "b6")
GROUP BY Origin, Dest
ORDER BY carriers.carrierName;
```

- 병렬 쿼리 OFF일때 걸린 시간: 6분 2.21초
- 병렬 쿼리 ON일때 걸린 시간: 16초

### 인스턴스 크기가 큰곳에서의 성능

#### 큰 인스턴스의 db로 변경

```bash
cd ~
mysql -u dbadmin -p -h qdgcjc71y0ak99.cosisna12bf9.us-west-2.rds.amazonaws.com

# MySql 접근후 DATABASE 변경
USE ontimeflights;
```

- 현재 rdb 서버 인스턴스 : db.r5.large

```sql
SET SESSION aurora_pq=0; -- 병렬쿼리 ON 시킬때는 1로 변경
SET SESSION aurora_pq_force=0; -- 병렬쿼리 ON 시킬때는 1로 변경

SELECT SQL_NO_CACHE
  carriers.carrierName AS 'Carrier',
  flightdata.Origin AS 'Origin Airport',
  flightdata.Dest AS 'Destination Airport',
  AVG(flightdata.ArrDelay) AS 'Average Arrival Delay',
  COUNT(flightdata.ArrDelay) AS 'Number of Delays',
  SUM(flightdata.Cancelled) AS 'Cancelled Flights'
FROM flightdata
LEFT JOIN carriers
ON carriers.carrierCode = flightdata.Reporting_Airline
WHERE flightdata.Distance < 1000
AND carriers.carrierCode IN ("AA", "UA", "DL", "b6")
GROUP BY Origin, Dest
ORDER BY carriers.carrierName;
```

- 병렬 쿼리 OFF일때 걸린 시간: 36.29 초
- 병렬 쿼리 ON일때 걸린 시간: 15.20초

### 결론

- 병렬쿼리는 인스턴스를 큰걸 쓸 필요없이 성능이 크게 향샹됩을 알 수 있다.

#### 최대 동시 병렬 쿼리 세션 보기

```sql
SHOW GLOBAL STATUS LIKE 'aurora_pq_max_concurrent_requests';
```

- 인스턴스유형이 클수록, 더 많은 동시 병렬 쿼리 세션이 제공된다.
- 최대 동시 병렬 쿼리 세션값은 인스턴스 크기에 따라 최대 16까지 이다.

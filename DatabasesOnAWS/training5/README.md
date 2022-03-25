# Amazon Redshift 데이터베이스 사용하기

```sql
BEGIN;

create schema if not exists imdb authorization adminuser;
set search_path = imdb;

COMMIT;
```

### 압축되지 않은 데이터 가져오기

```sql
BEGIN;

set search_path = imdb;

CREATE TABLE imdb.name_display (
"nameId" char(10) NOT NULL,
"name" varchar(128) NOT NULL,
"realName" varchar(255) DEFAULT NULL,
"akas" varchar(2000),
"image" varchar(192) DEFAULT NULL,
"imageId" char(12) DEFAULT NULL,
"nicknames" varchar(2000)
);

CREATE TABLE imdb.name_display_gzip (
"nameId" char(10) NOT NULL,
"name" varchar(128) NOT NULL,
"realName" varchar(255) DEFAULT NULL,
"akas" varchar(2000),
"image" varchar(192) DEFAULT NULL,
"imageId" char(12) DEFAULT NULL,
"nicknames" varchar(2000)
);

CREATE TABLE imdb.name_facts (
"nameId" char(10) NOT NULL,
"birthDate" date DEFAULT NULL,
"birthPlace" varchar(192) DEFAULT NULL,
"deathDate" date DEFAULT NULL,
"deathPlace" varchar(128) DEFAULT NULL,
"height" float DEFAULT NULL,
"gender" char(6) DEFAULT NULL,
"deathCause" varchar(128) DEFAULT NULL
);

CREATE TABLE imdb.name_facts_gzip (
"nameId" char(10) NOT NULL,
"birthDate" date DEFAULT NULL,
"birthPlace" varchar(192) DEFAULT NULL,
"deathDate" date DEFAULT NULL,
"deathPlace" varchar(128) DEFAULT NULL,
"height" float DEFAULT NULL,
"gender" char(6) DEFAULT NULL,
"deathCause" varchar(128) DEFAULT NULL
);

CREATE TABLE imdb.name_filmography (
"nameId" char(10) NOT NULL,
"ordering" integer NOT NULL,
"titleId" char(9) NOT NULL,
"category" varchar(32) NOT NULL,
"job" varchar(4000), -- You can use 'max' for the columns the values are big.
"status" varchar(19) DEFAULT NULL,
"attr" varchar(40) DEFAULT NULL,
"characters" varchar(2000),
"characterIds" varchar(2000),
"startYear" integer DEFAULT NULL,
"endYear" integer DEFAULT NULL,
"episodeCount" integer DEFAULT NULL
);

CREATE TABLE imdb.name_filmography_gzip (
"nameId" char(10) NOT NULL,
"ordering" integer NOT NULL,
"titleId" char(9) NOT NULL,
"category" varchar(32) NOT NULL,
"job" varchar(4000), -- You can use 'max' for the columns the values are big.
"status" varchar(19) DEFAULT NULL,
"attr" varchar(40) DEFAULT NULL,
"characters" varchar(2000),
"characterIds" varchar(2000),
"startYear" integer DEFAULT NULL,
"endYear" integer DEFAULT NULL,
"episodeCount" integer DEFAULT NULL
);

CREATE TABLE imdb.title_cast (
"titleId" char(9) NOT NULL,
"ordering" int NOT NULL,
"nameId" char(10) NOT NULL,
"category" char(15) NOT NULL,
"role" int DEFAULT NULL,
"characters" varchar(2500),
"characterIds" varchar(250),
"attributes" varchar(64) DEFAULT NULL
);

CREATE TABLE imdb.title_cast_gzip (
"titleId" char(9) NOT NULL,
"ordering" int NOT NULL,
"nameId" char(10) NOT NULL,
"category" char(15) NOT NULL,
"role" int DEFAULT NULL,
"characters" varchar(2500),
"characterIds" varchar(250),
"attributes" varchar(64) DEFAULT NULL
);

CREATE TABLE imdb.title_crew (
"titleId" char(9) NOT NULL,
"ordering" int NOT NULL,
"nameId" char(10) NOT NULL,
"category" varchar(28) DEFAULT NULL,
"job" varchar(4000),
"casting" varchar(192) DEFAULT NULL,
"attributes" varchar(32) DEFAULT NULL
);

CREATE TABLE imdb.title_crew_gzip (
"titleId" char(9) NOT NULL,
"ordering" int NOT NULL,
"nameId" char(10) NOT NULL,
"category" varchar(28) DEFAULT NULL,
"job" varchar(4000),
"casting" varchar(192) DEFAULT NULL,
"attributes" varchar(32) DEFAULT NULL
);

CREATE TABLE imdb.title_display (
"titleId" char(9) NOT NULL,
"title" text NOT NULL,
"year" int DEFAULT NULL,
"adult" int DEFAULT NULL,
"runtimeMinutes" int DEFAULT NULL,
"imageUrl" varchar(175) DEFAULT NULL,
"imageId" char(12) DEFAULT NULL,
"type" char(12) DEFAULT NULL,
"originalTitle" text
);

CREATE TABLE imdb.title_display_gzip (
"titleId" char(9) NOT NULL,
"title" text NOT NULL,
"year" int DEFAULT NULL,
"adult" int DEFAULT NULL,
"runtimeMinutes" int DEFAULT NULL,
"imageUrl" varchar(175) DEFAULT NULL,
"imageId" char(12) DEFAULT NULL,
"type" char(12) DEFAULT NULL,
"originalTitle" text
);

CREATE TABLE imdb.title_genres (
"titleId" char(10) NOT NULL,
"genres" varchar(250) NOT NULL
);

CREATE TABLE imdb.title_genres_gzip (
"titleId" char(10) NOT NULL,
"genres" varchar(250) NOT NULL
);

COMMIT;
```

```sql
BEGIN;

COPY imdb.name_display FROM 's3://(LabDataBucket)/name-display/split/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)';

COPY imdb.name_facts FROM 's3://(LabDataBucket)/name-facts/split/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)';

COPY imdb.name_filmography FROM 's3://(LabDataBucket)/name-filmography/split/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)';

COPY imdb.title_cast FROM 's3://(LabDataBucket)/title-cast/split/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)';

COPY imdb.title_crew FROM 's3://(LabDataBucket)/title-crew/split/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)';

COPY imdb.title_display FROM 's3://(LabDataBucket)/title-display/split/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)';

COPY imdb.title_genres FROM 's3://(LabDataBucket)/title-genres/split/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)';

COMMIT;
```

- 42.12s

### 압축된 데이터 가져오기

```sql
BEGIN;

COPY imdb.name_display_gzip FROM 's3://(LabDataBucket)/name-display/split-with-gzip/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)' gzip;

COPY imdb.name_facts_gzip FROM 's3://(LabDataBucket)/name-facts/split-with-gzip/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)' gzip;

COPY imdb.name_filmography_gzip FROM 's3://(LabDataBucket)/name-filmography/split-with-gzip/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)' gzip;

COPY imdb.title_cast_gzip FROM 's3://(LabDataBucket)/title-cast/split-with-gzip/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)' gzip;

COPY imdb.title_crew_gzip FROM 's3://(LabDataBucket)/title-crew/split-with-gzip/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)' gzip;

COPY imdb.title_display_gzip FROM 's3://(LabDataBucket)/title-display/split-with-gzip/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)' gzip;

COPY imdb.title_genres_gzip FROM 's3://(LabDataBucket)/title-genres/split-with-gzip/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)' gzip;

COMMIT;
```

- 27.81s

### 데이터 로드 테스트

```sql
select a.name, a.nameId, a.realName, c.title, c.year, c.runtimeMinutes, c.type, c.originalTitle, d.status
from imdb.name_display_gzip a, imdb.title_cast_gzip b, imdb.title_display_gzip c, imdb.name_filmography_gzip d
-- from imdb.name_display a, imdb.title_cast b, imdb.title_display c, imdb.name_filmography d -- 압축되지 않은 데이터 쿼리하기
where a.nameId = b.nameId
  and b.titleId = c.titleId
  and c.titleId = d.titleId
  and a.nameId = d.nameId
  and a.name = 'Tom Hanks';
```

- 압축된 데이터나 아닌 데이터나 쿼리하는데 시간 차이는 없었다.

## 작업 4: 매니페스트 파일을 이용해서 데이터 가져오기

```sql
BEGIN;

CREATE TABLE imdb.title_genres_mnf (
"titleId" char(10) NOT NULL,
"genres" varchar(250) NOT NULL
);

COMMIT;
```

```manifest
{
  "entries": [
    {"url":"s3://(LabDataBucket)/title-genres/split-with-gzip/tg_aa.gz", "mandatory":true},
    {"url":"s3://(LabDataBucket)/title-genres/split-with-gzip/tg_ab.gz", "mandatory":true},
    {"url":"s3://(LabDataBucket)/title-genres/split-with-gzip/tg_ac.gz", "mandatory":true}
  ]
}
```

```sql
BEGIN;

COPY imdb.title_genres_mnf FROM 's3://(LabDataBucket)/title_genres.manifest'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)' gzip manifest;

COMMIT;
```

### 확인하기

```sql
select count(*) as counts1
from imdb.title_genres_mnf;

select count(*) as counts2
from imdb.title_genres;
```

## 작업 5: 데이터 언로드

```sql
UNLOAD ('select * from imdb.name_filmography where titleid in (select titleid from imdb.title_display where year between 1990 and 1996)')
to 's3://(LabDataBucket)/unload/name-filmography/tf_'
iam_role '(RedshiftAccessRoleArn)' MAXFILESIZE 5MB;
```

## 작업 6: VACUUM 및 ANALYZE 명령 사용

```sql
BEGIN;
DELETE FROM imdb.name_filmography where titleid in (select titleid from imdb.title_display where year between 1990 and 1996);
COMMIT;
```

### VACUUM 작업 실행

```sql
SELECT  schema as table_schema, "table" as table_name, size, stats_off, tbl_rows, estimated_visible_rows
FROM svv_table_info d
WHERE "table" like 'name_filmography%';
```

```sql
set autocommit on;
VACUUM FULL imdb.name_filmography;
set autocommit off;
```

### ANALYZE 작업 실행

```sql
ANALYZE  verbose imdb.name_filmography;
```

## 작업 7: SORTKEY 및 DISTKEY를 사용한 최적화

```sql
BEGIN;

CREATE TABLE imdb.name_display_dskey (
"nameId" char(10) NOT NULL DISTKEY,
"name" varchar(128) NOT NULL,
"realName" varchar(255) DEFAULT NULL,
"akas" varchar(2000),
"image" varchar(192) DEFAULT NULL,
"imageId" char(12) DEFAULT NULL,
"nicknames" varchar(2000)
);
CREATE TABLE imdb.title_display_dskey(
"titleId" char(9) NOT NULL DISTKEY,
"title" text NOT NULL,
"year" int DEFAULT NULL,
"adult" int DEFAULT NULL,
"runtimeMinutes" int DEFAULT NULL,
"imageUrl" varchar(175) DEFAULT NULL,
"imageId" char(12) DEFAULT NULL,
"type" char(12) DEFAULT NULL,
"originalTitle" text
);
CREATE TABLE imdb.title_cast_dskey (
"titleId" char(9) NOT NULL DISTKEY,
"ordering" int NOT NULL,
"nameId" char(10) NOT NULL,
"category" char(15) NOT NULL,
"role" int DEFAULT NULL,
"characters" varchar(2500),
"characterIds" varchar(250),
"attributes" varchar(64) DEFAULT NULL
)
SORTKEY (titleid, ordering);

COMMIT;
```

```sql
BEGIN;

COPY imdb.title_cast_dskey FROM 's3://(LabDataBucket)/title-cast/split/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)';

COPY imdb.name_display_dskey FROM 's3://(LabDataBucket)/name-display/split/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)';

COPY imdb.title_display_dskey FROM 's3://(LabDataBucket)/title-display/split/'
iam_role '(RedshiftAccessRoleArn)'
delimiter '\t' timeformat 'YYYY-MM-DD HH:MI:SS' NULL AS 'NULL' region '(Region)';

COMMIT;
```

### DISTKEY 및 SORTKEY 테스트

#### 키없이 일반 질의

```sql
select b.title, a.name, c.ordering
from imdb.name_display a, imdb.title_display b,imdb.title_cast c
where a.nameid = c.nameid
  and b.titleid = c.titleid
order by c.titleid, c.ordering
```

- 14.61s

#### DISTKEY 및 SORTKEY 값으로 질의

```sql
select b.title, a.name, c.ordering
from imdb.name_display_dskey a, imdb.title_display_dskey b,imdb.title_cast_dskey c
where a.nameid = c.nameid
  and b.titleid = c.titleid
order by c.titleid, c.ordering
```

- 8.09s
- 응답시간이 개선되었음을 알 수 있다.

## 작업 8: 콘솔을 사용하여 쿼리 통계 보기


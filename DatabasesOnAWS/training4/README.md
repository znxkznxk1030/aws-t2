# Amazon DynamoDB 데이터베이스 사용하기

## 작업 1

```bash
cd ~
source ~/.bashrc
ls -ltrh
python3 createUpdate.py
```

### createUpdate.py

- DynamoDB로 부터 데이터를 가져와서 Cast 테이블을 생성하고 year열에 파티션 키를, title열에 정렬키를 할당합니다
- 총 데이터 개수는 85,437개

### .bashrc

```bash
# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
```

## 작업 2

```bash
aws dynamodb scan --table-name Cast \
  --filter-expression "genres = :a" \
  --projection-expression "#YR, #TT" \
  --expression-attribute-names file://expression-attribute-names.json \
  --expression-attribute-values file://expression-attribute-values.json

```

### expression-attribute-names.json

```json
{
  "#YR": "year",
  "#TT": "title"
}
```

### expression-attribute-values.json

```json
{
  ":a": { "S": "Sport" }
}
```

```bash
aws dynamodb get-item --table-name Cast \
    --key '{"year":{"N": "1999"},"title":{"S":"18 Shades of Dust"}}' \
    --expression-attribute-name '{"#c": "cast"}' \
    --projection-expression "titleId, title, runtimeMinutes, genres, #c"
```

## 작업 3

```bash
unzip TryDax.zip
cd TryDax/python

python3 01-create-table.py
python3 02-write-data.py
```

### DAX 클라이언트 없이 테이블 쿼리

```bash
python3 03-getitem-test.py
python3 04-query-test.py
python3 05-scan-test.py
```

- Total time: 33.50703740119934 sec - Avg time: 0.6701407480239868 sec
- Total time: 0.1063544750213623 sec - Avg time: 0.021270895004272462 sec
- Total time: 0.1171576976776123 sec - Avg time: 0.02343153953552246 sec
- 

### DAX 클라이언트 & 테이블 쿼리

```bash
aws dax describe-clusters --query "Clusters[*].ClusterDiscoveryEndpoint"

# {
#     "Address": "daxcluster.6pmbsa.dax-clusters.us-west-2.amazonaws.com",
#     "Port": 8111,
#     "URL": "dax://daxcluster.6pmbsa.dax-clusters.us-west-2.amazonaws.com"
# }
```

```bash
python3 03-getitem-test.py daxcluster.6pmbsa.dax-clusters.us-west-2.amazonaws.com:8111
python3 04-query-test.py daxcluster.6pmbsa.dax-clusters.us-west-2.amazonaws.com:8111
python3 05-scan-test.py daxcluster.6pmbsa.dax-clusters.us-west-2.amazonaws.com:8111
```

- Total time: 4.560556888580322 sec - Avg time: 0.09121113777160644 sec
- Total time: 0.043855905532836914 sec - Avg time: 0.008771181106567383 sec
- Total time: 0.19745421409606934 sec - Avg time: 0.03949084281921387 sec

## 작업 4

## 작업 5

## 부록

### createUpdate.py 소스코드

```python
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import time
import os

count = 0

session = boto3.session.Session()
region = session.region_name

dynamodb = boto3.resource('dynamodb', region_name=region)
table_name = 'Cast'   # table name
pk = 'year'           # primary key
sk = 'title'          # sort key
file_name = 'cast_full.json'

def create_table():
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': pk,
                    'KeyType': 'HASH'  #Partition key
                },
                {
                    'AttributeName': sk,
                    'KeyType': 'RANGE'  #Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'year',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },
            ],
            BillingMode='PAY_PER_REQUEST'
            #ProvisionedThroughput={
            #  'ReadCapacityUnits': 125,
            #  'WriteCapacityUnits': 125
            # }
        )
        print("Table status:", table.table_status)
    except:
        print("Table exist:Uploading data")
        table = dynamodb.Table('Cast')

def add_table():
    table = dynamodb.Table(table_name)
    count = 0
    with open(file_name) as json_file:
        movies = json.load(json_file, parse_float = decimal.Decimal)
        with table.batch_writer(overwrite_by_pkeys=[pk, sk]) as batch:
            for movie in movies:
                titleId = movie['titleId']
                title = movie['title']
                year = int(movie['year'])
                genres = movie['genres']
                runtimeMinutes = int(movie['runtimeMinutes'])
                cast = movie['cast']
                count = count + 1
                print("Adding record count:", count)
                batch.put_item(
                Item={
                    'titleId': titleId,
                    'year': year,
                    'title': title,
                    'genres': genres,
                    'runtimeMinutes': runtimeMinutes,
                    'cast': cast,
                    }
                )
def main():
    create_table()
    add_table()

if __name__ == "__main__":
    main()

```

### scan.py 소스코드

```python
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

table_name = 'Cast'
pk = 'year'
sk = 'title'

session = boto3.session.Session()
region = session.region_name

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name=region)

table = dynamodb.Table(table_name)

fe = Key(pk).between(1990, 1991) & Key(sk).between('A', 'D')
pe = "#yr, title, #ca"
ean = { "#yr": "year", "#ca": "cast",}
esk = None

response = table.scan(
    FilterExpression=fe,
    ProjectionExpression=pe,
    ExpressionAttributeNames=ean
    )

for i in response['Items']:
    print(json.dumps(i, cls=DecimalEncoder))

while 'LastEvaluatedKey' in response:
    response = table.scan(
        ProjectionExpression=pe,
        FilterExpression=fe,
        ExpressionAttributeNames= ean,
        ExclusiveStartKey=response['LastEvaluatedKey']
        )
    #parsing and printing the JSON response
    for i in response['Items']:
        print(i['year'], ":", i['title'] + " and the actors are:")
        for j in i['cast']:
            print(j['name'])
        print('\n')
```

### query.py 소스코드

```python
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

session = boto3.session.Session()
region = session.region_name
table_name = 'Cast'
pk = 'year'
sk = 'title'

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name=region)

table = dynamodb.Table(table_name)

print("Movies in 2005 - titles A-L, and list of actors")

response = table.query(
    ProjectionExpression="#yr, title, #ca",
    ExpressionAttributeNames={ "#yr": "year", "#ca": "cast" },
    KeyConditionExpression=Key(pk).eq(2005) & Key(sk).between('A', 'L')
)

for i in response['Items']:
        print(i['year'], ":", i['title'] + " and the actors are:")
        for j in i['cast']:
            print(j['name'])
        print('\n')
```

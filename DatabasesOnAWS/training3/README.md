# Amazon DocumentDB 데이터베이스 사용하기

```bash
cd ~

mongoimport --ssl --host mydocdb.cluster-c2ghwu0izgvh.us-west-2.docdb.amazonaws.com:27017 \
 --sslCAFile rds-combined-ca-bundle.pem \
 --username docdbadmin \
 --password Pa33w0rd! \
 --collection cast_1990 --db cast \
 --file /tmp/cast_1990.json --jsonArray
```

```python
import os
import glob
from pymongo import MongoClient
import json
import sys
x = 1990

DATABASE_NAME = 'cast'

client = MongoClient('mongodb:///docdbadmin:Pa33w0rd!
                    @mydocdb.cluster-c2ghwu0izgvh.us-west-2.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=/home/ssm-user/
                    rds-combined-ca-bundle.pem&replicaSet=rs0')

filelist = []
for file in glob.glob("/tmp/*.json"):
    filelist.append(file)

filelist.sort()

for item in filelist:
    print(item)
    f = open(item, 'r')
    jsonData = json.loads(f.read())
    db = client[DATABASE_NAME] #Connect to specific database
    col_name = "cast_"+str(x)
    collection = db[col_name] #Access specific collection
    collection_id = collection.insert_many(jsonData)
    x = x + 1
    #return x
    client.close()

```

```bash
mongo --ssl --host mydocdb.cluster-c2ghwu0izgvh.us-west-2.docdb.amazonaws.com:27017 \
--sslCAFile rds-combined-ca-bundle.pem \
--username docdbadmin \
--password Pa33w0rd!
```

```mongo
show dbs;

use cast;
show collections;

db.cast_1990.findOne()
```

## 작업 2:

### 1990 - 2005 년사이의 배우가 캐스팅된 횟수를 구하는 람다함수

```python
import json
import pymongo
import boto3
import base64
import configparser
import os
import ast
from botocore.exceptions import ClientError
from botocore.vendored import requests

secret_name = os.environ['secret_name']
region_name = os.environ['region']
document_db_port=os.environ['db_port']
pem_locator=os.environ['pem_locator']

session = boto3.session.Session()
client = session.client(service_name='secretsmanager',
         region_name=region_name)

get_secret_value_response = "null"
#GET THE SECRET

try:
    get_secret_value_response =client.get_secret_value(SecretId=secret_name)
except ClientError as e:
    raise e

secret_data = json.loads(get_secret_value_response['SecretString'])

username = secret_data['username']
password = secret_data['password']
docdb_host=secret_data['host']

db_client = pymongo.MongoClient('mongodb://'+username+':'+password+'@'+
docdb_host+':'+document_db_port+'/?ssl=true&ssl_ca_certs='+pem_locator)

def lambda_handler(event, context):
    httpmethod = event["httpMethod"]
    queryval=''
    if httpmethod == "GET" :
        print(event['body'])
        query=(event['body'])
    else :
        print(event['body'])
        query=(event['body'])
    print("Query type " + query)
    querylower=queryval.lower()
    errorstring="Invalid Query, please pass 'total number of events',
    'number of mentions for {keyword}, most talked event"
    return_val= {
                "isBase64Encoded": "true",
                "statusCode": 200,
                "headers": { "headerName": "headerValue"},
                "body": errorstring
            } #A simple error message for usage, Just to get the body right
    try:
        db = db_client['cast']
        querydict = json.loads(query)
        print(querydict)
        countMovies = 0
        print(db.collection_names())
        for quest in db.collection_names():
            print(quest)
            queryString = db[quest].find(querydict)
            counttotal = queryString.count()
            countMovies = countMovies + counttotal
        return_val['body'] = "Movie Count is "+str(countMovies)
        return return_val
    except Exception as ex:
        # Send some context about this error to Lambda Logs
        print(ex)
```

- cluster: mydocdb
  - dbinstancea-fcwcadcql7ng
  - dbinstanceb-dmxwvawy36bg

```bash
cd ~
aws docdb describe-db-clusters \
    --db-cluster-identifier mydocdb  \
    --query 'DBClusters[*].[DBClusterIdentifier,Status]'
```

```bash
aws docdb describe-db-instances \
    --db-instance-identifier dbinstancea-fcwcadcql7ng  \
    --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceStatus]'
```

## 작업 4

## 작업 5

```bash
mongodb://docdbadmin:Pa33w0rd!@mydocdb.cluster-c2ghwu0izgvh.us-west-2.docdb.amazonaws.com:27017/?ssl=true&ssl_ca_certs=rds-combined-ca-bundle.pem&replicaSet=rs0
```

### mongoAdmin

```json
{
  "name": "Martha Rivera",
  "title": "Manager",
  "region": "North East",
  "Address": [{ "street": "100 Main Street", "state": "CA", "zip": 22222 }]
}
```

### 장애조치 시뮬레이션

## 부록

### 1990~2005 사이의 멧데이먼의 영화의 개수

```javascript
resultCount = 0;
db.getCollectionNames().forEach(function (collection) {
  resultCount =
    resultCount + db[collection].find({ "cast.name": "Matt Damon" }).count();
});
print("Total Movies Played between 1990 to 2005: " + resultCount);
```

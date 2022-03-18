# 실습 3 - DynamoDB

## Error 리스트

### 1.11.3xx버전이 먹지 않음 => 404버전으로 업그레이드

```xml
<dependencyManagement>
  <dependencies>
   <dependency>
    <groupId>com.amazonaws</groupId>
    <artifactId>aws-java-sdk-bom</artifactId>
    <version>1.11.404</version>
    <type>pom</type>
    <scope>import</scope>
   </dependency>
  </dependencies>
</dependencyManagement>
```

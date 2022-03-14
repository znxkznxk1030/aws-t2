# 실습 2 – AWS에서 웹 애플리케이션 배포

## 보안 구성

![보안구성 - 1](./figures/ec2-1.png)
![보안구성 - 2](./figures/ec2-2.png)
![보안구성 - 3](./figures/ec2-3.png)
![보안구성 - 4](./figures/ec2-4.png)
![보안구성 - 5](./figures/ec2-5.png)

## Amazon RDS 데이터 베이스 생성

![데이터 베이스 생성 - 1](./figures/ec2-6.png)
![데이터 베이스 생성 - 1](./figures/ec2-7.png)
![데이터 베이스 생성 - 1](./figures/ec2-8.png)
![데이터 베이스 생성 - 1](./figures/ec2-9.png)
![데이터 베이스 생성 - 1](./figures/ec2-10.png)
![데이터 베이스 생성 - 1](./figures/ec2-11.png)
![데이터 베이스 생성 - 1](./figures/ec2-12.png)
![데이터 베이스 생성 - 1](./figures/ec2-13.png)

## Amazon EC2를 사용하여 애플리케이션 서버 시작

![Amazon EC2를 사용 - 1](./figures/ec2-14.png)
![Amazon EC2를 사용 - 2](./figures/ec2-15.png)
![Amazon EC2를 사용 - 3](./figures/ec2-16.png)
![Amazon EC2를 사용 - 4](./figures/ec2-17.png)
![Amazon EC2를 사용 - 5](./figures/ec2-18.png)

- Inventory-App-Role

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "ssm:*",
      "Resource": "arn:aws:ssm:*:*:parameter/inventory-app/*",
      "Effect": "Allow"
    }
  ]
}
```

- user data

```bash
#!/bin/bash
# Install Apache Web Server and PHP
yum install -y httpd mysql
amazon-linux-extras install -y php7.2
# Download Lab files
wget https://us-west-2-tcprod.s3.amazonaws.com/courses/ILT-TF-200-ARCHIT/v6.8.28/lab-2-webapp/scripts/inventory-app.zip
unzip inventory-app.zip -d /var/www/html/
# Download and install the AWS SDK for PHP
wget https://github.com/aws/aws-sdk-php/releases/download/3.62.3/aws.zip
unzip aws -d /var/www/html
# Turn on web server
chkconfig httpd on
service httpd start
```

![Amazon EC2를 사용 - 6](./figures/ec2-19.png)
![Amazon EC2를 사용 - 7](./figures/ec2-20.png)
![Amazon EC2를 사용 - 8](./figures/ec2-21.png)
![Amazon EC2를 사용 - 9](./figures/ec2-22.png)
![Amazon EC2를 사용 - 10](./figures/ec2-23.png)
![Amazon EC2를 사용 - 11](./figures/ec2-24.png)

## 애플리케이션 테스트

![애플리케이션 테스트 - 1](./figures/ec2-25.png)
![애플리케이션 테스트 - 2](./figures/ec2-26.png)
![애플리케이션 테스트 - 2](./figures/ec2-27.png)

# microservices-backend
First microservices architecture application for AI backend API

## Used technologies
- Java
- Spring Boot
- Python
- Docker
- python logging
- RabbitMQ
- SMTP
- Firebase

TODO:
- Kubernetes
- Fast API
- AI
- Python Telegram bot
- Log4j
- MongoDB
- NGINX
- JWT/OAuth 2.0/TLS/API Authorization
- AWS/Azure/GCP/Linode/Digital Ocean (for cloud providing)
- Graphana/Kibana/Prometheus (for monitoring)
- Jenkins/Gitlab
- NGINX

(choose one for every technology)

## Features
TODO

## How to run projects
### Creating JAR file(main service)
First of all you must to create JAR file for main application(API service)

1. Using Intellij IDEA
* Open project folder
* Open Maven tools window(View -> Tool Windows -> Maven)
* Double click on 'package'

2. Using terminal
* Open terminal in main project folder($project-path/main)
* Type ```mvn package```

### Configuring mail service
For the mail service to work correctly, you need to create a .env file with authorization data. But before this, you must configure your email account

For more information visit this site:
(link)

1. Create .env file in mail service directory($project-path/mail)

2. Insert the following fragment into the file:
```
EMAIL=""
PASSWORD=""
```

3. Inside double quotes(") write your authorization data

### Configure Firebase
For this project we are using Firebase as a DB where we store images from users

To create your own database and use it in this project, watch the video at [this link](https://www.youtube.com/watch?v=c7OCGzJ_8aU)

* Then you need to create an .env file and insert following text:
```
API_KEY=
```
* And after '=' insert your API_KEY from Firebase

### Start project
After that, you finaly can start project

* Open terminal in root directory($project-path)
* Type ```docker compose up --build```

First time it may takes a litle time to start

## Download links
TODO

# microservices-backend
First microservices architecture application for AI backend API

## Used technologies
- Java
- Spring Boot
- Python
- Docker
- Kubernetes
- Log4j
- python logging
- MongoDB
- MySQL/Firebase
- RabbitMQ
- JWT/OAuth 2.0/TLS/API Authorization
- AWS/Azure/GCP/Linode/Digital Ocean (for cloud providing)
- Graphana/Kibana/Prometheus (for monitoring)
- Jenkins/Gitlab

(choose one for every technology)

## Features
- [x] Add to docker-compose file line for build every app before staring
- [x] Add condition for main container to run after RabbitMQ fully started

## How to run projects
### Creating JAR file
First of all you must to create JAR file for main application(API service)

1. Using Intellij IDEA
* Open project folder
* Open Maven tools window(View -> Tool Windows -> Maven)
* Double click on 'package'

2. Using terminal
* Open terminal in main project folder($project-path/main)
* Type ```mvn package```

### Start project
After that, you finaly can start project

* Open terminal in backend directory($project-path)
* Type ```docker compose up```

First time it may takes a litle time to start

## Download links
TODO

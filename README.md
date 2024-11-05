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

##Features
- [ ] Add to docker-compose file line for build every app before staring
- [ ] Add condition for main container to run after RabbitMQ fully started

## How to run projects
First of all, lets create JAR file for main application(API service)

1.1 Using Intellij IDEA
    * Open project folder
    * Open Maven tools window(View -> Tool Windows -> Maven)
    * Double click on 'package'
1.2 Using terminal
    * Open terminal in main project folder({project-path}/backend/main)
    * Type ```mvn package```

Now you have JAR file.
<!-- Убрати компіляцію через ручний ввід docker 'build -t main .', щоб docker-compose файл сам все робив -->
Then, lets build main container
* In main folder type in terminal
    ```docker build -t main .```

After that, you finaly can start project
* Open terminal in backend directory({project-path}/backend)
* Type in terminal
    ```docker compose up```
First time it may takes a litle time to start

## Download links
TODO

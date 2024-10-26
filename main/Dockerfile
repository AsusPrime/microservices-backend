FROM openjdk:22
EXPOSE 8080
WORKDIR /app
COPY target/main-0.0.1-SNAPSHOT.jar app.jar
CMD ["java", "-jar", "app.jar"]
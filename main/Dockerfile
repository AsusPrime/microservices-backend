FROM openjdk:22
EXPOSE 8080
WORKDIR /app
COPY out/artifacts/main_jar/main.jar app.jar
CMD ["java", "-jar", "app.jar"]
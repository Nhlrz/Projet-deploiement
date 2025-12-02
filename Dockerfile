FROM alpine:latest

CMD echo "Bonjour Polytech Nancy" 


FROM eclipse-temurin:21-jdk AS build
COPY Hello.java

RUN javac HELLO.java

FROM eclipse-temurin:21-jre

WORKDIR /app

COPY --from=build /app/Hello.class

CMD ["java", "Hello"]

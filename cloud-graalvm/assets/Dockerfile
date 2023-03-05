FROM vegardit/graalvm-maven:22.3.1-java11 AS builder
WORKDIR /build
COPY addressbook .
RUN mkdir src
RUN mv main/ src/
RUN mvn -Pnative native:compile -s settings.xml

FROM alpine
WORKDIR /app
RUN mkdir /app/config
COPY --from=builder /build/target/addressbook /app/app
EXPOSE 8080/tcp
CMD ["./app"]
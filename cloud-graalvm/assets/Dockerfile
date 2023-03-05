FROM registry.access.redhat.com/quarkus/mandrel-22-rhel8:22.3-10.1675794341 AS builder
WORKDIR /build
COPY addressbook .
RUN ./mvnw -Pnative native:compile

FROM registry.access.redhat.com/ubi9/ubi-minimal:9.1.0-1793
WORKDIR /app
RUN mkdir /app/config
COPY --from=builder /build/target/addressbook /app/app
EXPOSE 8080/tcp
CMD ["./app"]
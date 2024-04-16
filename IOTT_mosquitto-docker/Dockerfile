# syntax = docker/dockerfile:1
# Use openssl instead of latest as latest does not support encryption
# RUN mosquitto_passwd -c -b /mosquitto/config/pwfile rpimqttclient V2HZX4S4UD64A7YH
FROM eclipse-mosquitto:openssl
WORKDIR /mosquitto
#COPY mosquitto-config mosquitto-config/
COPY mosquitto-config config
RUN mosquitto_passwd -c -b /mosquitto/config/mosquitto-password.txt rpimqttclient-sensehat pD2l0bYEw
EXPOSE 8883 8883

#!/bin/ash

apk update
apk add make
pip install -r requirements.txt
adduser -u 1000 -D py
sleep inf
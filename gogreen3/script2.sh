#!/bin/bash
clear
cd /home/pi/versao3/gogreen3
python3 gateway.py &
python3 subscriber_local.py &


#!/bin/bash

curl --data "username=$1&trolly_id=$2" http://localhost:8000/trolly/occupy/
#curl --data "username=$1&trolly_id=$2" http://185.205.209.236:8000/trolly/occupy/
#!/bin/bash

curl --data "id=$1&x=$2&y=$3&isOccupied=$4&last_update=$5" http://localhost:8000/trolly/add/
# curl --data "x=$1&y=$2&isOccupied=$3&last_update=$4" http://185.205.209.236:8000/trolly/add/

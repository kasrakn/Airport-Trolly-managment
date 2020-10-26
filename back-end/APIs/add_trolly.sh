#!/bin/bash

curl --data "x=$1&y=$2&isOccupied=$3&last_update=$4" http://localhost:8000/register/trolly/
# curl --data "x=$1&y=$2&isOccupied=$3&last_update=$4" http://185.205.209.236:8000/register/trolly/
 
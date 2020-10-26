#!/bin/bash

curl --data "username=$1&email=$2&phone_number=$3&password=$4" http://localhost:8000/register/user
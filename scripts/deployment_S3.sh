#!/bin/sh

if aws s3 ls "s3://vogaeventrecorderstack" 2>&1 | grep -q 'NoSuchBucket'
then
aws s3api create-bucket --bucket vogaeventrecorderstack --region eu-west-1
fi
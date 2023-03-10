#!/bin/sh

if aws s3 ls "s3://voga-event-recorder-stack" 2>&1 | grep -q 'NoSuchBucket'
then
aws s3api create-bucket --bucket voga-event-recorder-stack --region eu-west-1 --create-bucket-configuration LocationConstraint=eu-west-1
aws s3api put-public-access-block \
    --bucket voga-event-recorder-stack  \
    --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
fi
#!/bin/bash

export OVERRIDE_S3_ENDPOINT='http://127.0.0.1:9000/'
export SOURCE_BUCKET='dataexports'
export SOURCE_PATH='s3://dataexports/csv_data/stark_doc_data.csv'
export access='minioadmin'
export secret='minioadmin'
export region='ap-south-1'
export REDIS_ENDPOINT='redis://localhost:6379'
export RESUME_SOURCE_PATH='s3://datasets/csv_data/resume_data.csv'
export RESUME_BUCKET='resumes'

export SQLDBURI='postgresql+psycopg2://postgres:123456789@localhost:5432/stark_dev_test'
export USER='root'
export PASSWORD='123456789'
export HOST='127.0.0.1:3306'
export DB='stark_dev'

echo -e "******************************RION-Stark****************************"
python3 main.py main:app --reload --port 5001
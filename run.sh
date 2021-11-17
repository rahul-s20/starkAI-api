export OVERRIDE_S3_ENDPOINT='http://127.0.0.1:9000/'
export SOURCE_BUCKET='dataexports'
export SOURCE_PATH='s3://dataexports/csv_data/stark_doc_data.csv'
export access='minioadmin'
export secret='minioadmin'
export region='ap-south-1'

export USER='root'
export PASSWORD='123456789'
export HOST=1'27.0.0.1:3306'
export DB='stark_dev'

echo -e "******************************RION-Stark****************************"
python main.py main:app --reload --port 5001
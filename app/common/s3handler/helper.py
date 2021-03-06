import awswrangler as wr
import boto3
from os import environ as env
from botocore.client import Config
from io import BytesIO
from app.common.helpers.pdf_reader import extract_text_pdf_s3


class S3_Helper:
    def __init__(self, aws_secret: str = None, aws_access: str = None, end_point: str = None, region_name: str = None):
        if end_point is not None:
            wr.config.s3_endpoint_url = end_point
            self.boto3_session = boto3.Session(aws_access_key_id=aws_access,
                                               aws_secret_access_key=aws_secret,
                                               region_name=region_name)

            self.s3_resource = boto3.resource('s3', endpoint_url=env['OVERRIDE_S3_ENDPOINT'],
                                              aws_access_key_id=env['access'],
                                              aws_secret_access_key=env['secret'],
                                              region_name=env['region'],
                                              config=Config(signature_version='s3v4'))
        else:
            self.boto3_session = boto3.Session(aws_access_key_id=aws_access,
                                               aws_secret_access_key=aws_secret)
            self.s3_resource = boto3.resource('s3', aws_access_key_id=env['access'],
                                              aws_secret_access_key=env['secret'],
                                              region_name=env['region'])

    def read_csv_s3(self, src_path: str):
        try:
            data = wr.s3.read_csv(f"{src_path}", boto3_session=self.boto3_session, encoding='utf-8')
            return data
        except Exception as er:
            print(f"error: Unable to read csv: {er}")
            return None

    def read_pdf_s3(self, bucket_name: str, file_name: str):
        try:
            obj = self.s3_resource.Object(bucket_name, file_name)
            fs = obj.get()['Body'].read()
            text = extract_text_pdf_s3(BytesIO(fs))
            return text
        except Exception as er:
            print(f"error: Unable to read csv: {er}")
            return None

    def upload_s3(self, files, bucket_name: str) -> bool:
        try:
            s3bucket = self.s3_resource.Bucket(bucket_name)
            if len(files) > 0:
                for file in files:
                    s3bucket.put_object(Key=f'{file.filename}', Body=file.file._file, ACL='public-read')
            return True
        except Exception as er:
            print(f"Upload not working: {er}")
            return False

    def get_file_s3(self, filename, bucket_name: str):
        try:
            get_obj = self.s3_resource.Object(bucket_name, filename)
            downloaded_obj = get_obj.get()["Body"]
            return downloaded_obj
        except Exception as er:
            print(f"Get object is not working: {er}")
            return None

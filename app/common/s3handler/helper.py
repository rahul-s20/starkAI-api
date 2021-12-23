import awswrangler as wr
import boto3


class S3_Helper:
    def __init__(self, aws_secret: str = None, aws_access: str = None, end_point: str = None, region_name: str = None):
        if end_point is not None:
            wr.config.s3_endpoint_url = end_point
            self.boto3_session = boto3.Session(aws_access_key_id=aws_access,
                                               aws_secret_access_key=aws_secret,
                                               region_name=region_name)
        else:
            self.boto3_session = boto3.Session(aws_access_key_id=aws_access,
                                               aws_secret_access_key=aws_secret)

    def read_csv_s3(self, src_path: str):
        try:
            data = wr.s3.read_csv(f"{src_path}", boto3_session=self.boto3_session, encoding='utf-8')
            return data
        except Exception as er:
            print(f"error: Unable to read csv: {er}")
            return None

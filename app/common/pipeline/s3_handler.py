import awswrangler as wr
import boto3


class Inventory:

    def __init__(self, aws_secret: str = None, aws_access: str = None, end_point: str = None, region_name: str = None):
        if end_point is not None:
            wr.config.s3_endpoint_url = end_point
            self.boto3_session = boto3.Session(aws_access_key_id=aws_access,
                                               aws_secret_access_key=aws_secret,
                                               region_name=region_name)
        else:
            self.boto3_session = boto3.Session(aws_access_key_id=aws_access,
                                               aws_secret_access_key=aws_secret)

    def read_files(self, bucket: str = None, key: str = None, header = None):
        """
        s3://datasets/csv_data/stark_doc_data.csv
        :param bucket: datasets
        :param key: csv_data/stark_doc_data.csv
        :return:
        """
        try:
            data = wr.s3.read_csv(f"s3://{bucket}/{key}", boto3_session=self.boto3_session, header=header)
            return data
        except Exception as er:
            print(f"error: Unable to read csv: {er}")
            return None

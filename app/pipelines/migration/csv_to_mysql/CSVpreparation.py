from app.common.pipeline.s3_handler import Inventory
from app.common.pipeline.generate_primaryKey import generate_primaryKey
import pandas as pd


class CSVToDf:
    def __init__(self, endpoint: str = None, accesskey: str = None, secretkey: str = None, region: str = None):
        if endpoint is not None:
            self._iv = Inventory(end_point=endpoint, aws_access=accesskey, aws_secret=secretkey, region_name=region)
        else:
            self._iv = Inventory(aws_access=accesskey, aws_secret=secretkey)

    def prepareCSVdf(self, bucket: str = None, key: str = None, columns: list = [], default_values: str = "missing",
                     add_primaryKey: bool = False):
        try:
            if bucket and key is not None:
                csvDataframe = self._iv.read_files(bucket=bucket, key=key)
                is_Nan_values = csvDataframe.isnull().values.any()
                is_Nan_values = bool(is_Nan_values)
                if is_Nan_values is True:
                    csvDataframe = csvDataframe.fillna(default_values, inplace=True)
                if len(columns) == len(csvDataframe.columns):
                    csvDataframe.columns = columns
                if add_primaryKey is True:
                    _ids = generate_primaryKey(length=len(csvDataframe))
                    csvDataframe.insert(loc=0,
                                        column='ids',
                                        value=_ids)
                csvDataframe.insert(loc=0, column='timestamp', value=pd.to_datetime('now').replace(microsecond=0))
                return csvDataframe
        except Exception as ex:
            return ex.__cause__

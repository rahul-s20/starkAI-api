from app.common.s3handler.helper import S3_Helper
from os import environ as env


def io_symptoms():
    s3h = S3_Helper(env['secret'], env['access'], env['OVERRIDE_S3_ENDPOINT'], env['region'])
    data = s3h.read_csv_s3(src_path=env['SOURCE_PATH'])
    i_data = data.iloc[:, 1:19].values
    o_data = data.iloc[:, :1].values
    return i_data, o_data

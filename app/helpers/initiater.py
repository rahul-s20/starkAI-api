from app.common.s3handler.helper import S3_Helper
from os import environ as env
import seaborn as sns
import matplotlib.pyplot as plt


def io_symptoms():
    s3h = S3_Helper(env['secret'], env['access'], env['OVERRIDE_S3_ENDPOINT'], env['region'])
    data = s3h.read_csv_s3(src_path=env['SYMPTOMPS_SOURCE_PATH'])
    i_data = data.iloc[:, 1:19].values
    o_data = data.iloc[:, :1].values
    return i_data, o_data


def io_ResumeScreening():
    s3h = S3_Helper(env['secret'], env['access'], env['OVERRIDE_S3_ENDPOINT'], env['region'])
    data = s3h.read_csv_s3(src_path=env['RESUME_SOURCE_PATH'])
    data['cleaned_resume'] = ''
    unique_categories = data['Category'].unique()
    counts_unique_category = data['Category'].value_counts()
    # plt.figure(figsize=(15, 15))
    # plt.xticks(rotation=90)
    # sns.countplot(y="Category", data=data)
    # plt.show()


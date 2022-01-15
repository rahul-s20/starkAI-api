from app.common.s3handler.helper import S3_Helper
from os import environ as env
import re
from sklearn.preprocessing import LabelEncoder
from pandas import DataFrame


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
    data['cleaned_resume'] = data.Resume.apply(lambda x: cleanDataset(x))
    return data


def cleanDataset(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ',
                        resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText


def word_encoder(var_mode: list, dataset: DataFrame) -> DataFrame:
    le = LabelEncoder()
    if len(var_mode) > 0:
        for i in var_mode:
            dataset[i] = le.fit_transform(dataset[i])
        return dataset[i]
    else:
        return None

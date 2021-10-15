from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


class Vectorizer:
    def __init__(self):
        self.CV = CountVectorizer()

    def vectorized(self, i_data: np.ndarray, transform_type: str = 'fit_transform'):
        output_list = []
        for i in i_data.tolist():
            a = ' '.join(map(str, i))
            output_list.append(a)
        if transform_type is 'fit_transform':
            return self.CV.fit_transform(output_list)
        else:
            return self.CV.transform(output_list)


def encoder(columns: list, remainder: str, i_data: list):
    ct = ColumnTransformer(transformers=[
        ('encoder', OneHotEncoder(), columns)],
        remainder=remainder)
    encoded_data = np.array(ct.fit_transform(i_data).toarray())
    return encoded_data


def missingDataHandler(i_data: np.ndarray = None, o_data: np.ndarray = None, strategy: str = 'mean'):
    if strategy == 'constant':
        si = SimpleImputer(missing_values=np.nan, strategy=strategy, fill_value='NA')
    else:
        si = SimpleImputer(missing_values=np.nan, strategy=strategy)
    i_data = si.fit_transform(i_data[:, :])
    o_data = si.fit_transform(o_data[:, :])
    return i_data, o_data


def single_missingDataHandler(i_data: np.ndarray = None, strategy: str = 'mean'):
    if strategy == 'constant':
        si = SimpleImputer(missing_values=np.nan, strategy=strategy, fill_value='NA')
    else:
        si = SimpleImputer(missing_values=np.nan, strategy=strategy)
    i_data = si.fit_transform(i_data[:, :])
    return i_data

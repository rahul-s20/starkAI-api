import numpy as np
import pandas as pd


def input_data_scaling(i_data: list) -> list:
    if len(i_data) < 17:
        shortfall = 17 - len(i_data)
        i_data += shortfall * [np.nan]
    return [i_data]


def input_data_conversion_symptom(i_data: list) -> list:
    dataset = pd.DataFrame(i_data, columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
    data = dataset.iloc[:, 0:18].values
    return data

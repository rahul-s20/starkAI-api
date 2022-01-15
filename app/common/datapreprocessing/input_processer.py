import numpy as np
import pandas as pd
from nltk.corpus import stopwords
import string
import wordcloud
from pandas import DataFrame
from app.helpers.initiater import cleanDataset
import nltk


def input_data_scaling(i_data: list) -> list:
    if len(i_data) < 17:
        shortfall = 17 - len(i_data)
        i_data += shortfall * [np.nan]
    return [i_data]


def input_data_conversion_symptom(i_data: list) -> list:
    dataset = pd.DataFrame(i_data, columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
    data = dataset.iloc[:, 0:18].values
    return data


def resume_dataPreprocessor(resumeDataSet: DataFrame):
    oneSetofStopWrds = set(stopwords.words('english') + ['``', "''"])
    totalWords = []
    Sentences = resumeDataSet['Resume'].values
    cleanedSentences = ""
    for i in range(0, 160):
        cleanText = cleanDataset(Sentences[i])
        cleanedSentences += cleanText
        requiredWords = nltk.word_tokenize(cleanText)
        for word in requiredWords:
            if word not in oneSetofStopWrds and word not in string.punctuation:
                totalWords.append(word)

    wordfreqdist = nltk.FreqDist(totalWords)
    mostcommon = wordfreqdist.most_common(50)  # to check each word frequency

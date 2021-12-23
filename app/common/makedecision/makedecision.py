import numpy as np
from sklearn.ensemble import RandomForestClassifier
from app.common.datapreprocessing.preprocessing import missingDataHandler, single_missingDataHandler, convert_to_list
from sklearn import model_selection, svm
import joblib
from sklearn.feature_extraction.text import CountVectorizer


class Decision:
    def __init__(self, n_estimators: int = 100, criterion: str = 'entropy'):
        self.rf = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, random_state=0)
        self.col_arr = []
        self.CV = CountVectorizer(min_df=1, ngram_range=(1, 3), max_features = 30000)

    def saveSymptomModel(self, i_data: np.ndarray, o_data: np.ndarray, strategy: str = 'mean'):
        try:
            X, Y = missingDataHandler(i_data, o_data, strategy=strategy)
            data_list = convert_to_list(X)
            vectorized_X = self.CV.fit_transform(data_list)
            X_train, X_test, Y_train, Y_test = model_selection.train_test_split(vectorized_X, Y.ravel(), test_size=0.25,
                                                                                random_state=7)
            self.rf.fit(X_train, Y_train)
            vectorized_filename = 'DataModels/SymptomModel_vector.sav'
            joblib.dump(self.CV, vectorized_filename)
            model_filename = 'DataModels/SymptomModel.sav'
            joblib.dump(self.rf, model_filename)
            return 'Symptom model is saved successfully'
        except Exception as er:
            return er

    def deciderV2(self, strategy: str = 'mean', input_data=None):
        try:
            loaded_vectorizer = joblib.load('DataModels/SymptomModel_vector.sav')
            clf = joblib.load('DataModels/SymptomModel.sav')
            handled_input_data = single_missingDataHandler(input_data, strategy=strategy)
            predicted_data = clf.predict(loaded_vectorizer.transform(handled_input_data[0]))
            return predicted_data[0]
        except Exception as err:
            return f"Decision maker error: {err}"

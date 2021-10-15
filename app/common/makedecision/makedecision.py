import numpy as np
from sklearn.ensemble import RandomForestClassifier
from app.common.datapreprocessing.preprocessing import missingDataHandler, Vectorizer, single_missingDataHandler


class Decision:
    def __init__(self, n_estimators: int = 100, criterion: str = 'entropy'):
        self.rf = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, random_state=0)
        self.col_arr = []

    def decider(self, i_data: np.ndarray, o_data: np.ndarray, strategy: str = 'mean',
                input_data=None):
        vz = Vectorizer()
        try:
            X, Y = missingDataHandler(i_data, o_data, strategy=strategy)
            vectorized_X = vz.vectorized(i_data=X)
            self.rf.fit(vectorized_X, Y.ravel())
            handled_input_data = single_missingDataHandler(input_data, strategy=strategy)
            xo = vz.vectorized(i_data=handled_input_data, transform_type='transform')
            predicted_data = self.rf.predict(xo)
            return predicted_data[0]
        except Exception as err:
            print(f"Decision maker error: {err}")
            return None

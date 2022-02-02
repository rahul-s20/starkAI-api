from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
import joblib
import pandas as pd


class ResumeDecisionMaker:
    def __init__(self):
        self.tfv = TfidfVectorizer(sublinear_tf=True, stop_words='english', max_features=1500)
        self.clf = OneVsRestClassifier(KNeighborsClassifier())

    def save_resume_model(self, resume_df: pd.DataFrame) -> str:
        try:
            requiredText = resume_df['cleaned_resume'].values
            requiredTarget = resume_df['Category'].values
            WordFeatures = self.tfv.fit_transform(requiredText)
            print(requiredText)
            X_train, X_test, Y_train, Y_test = train_test_split(WordFeatures, requiredTarget, random_state=42,
                                                                test_size=0.2, shuffle=True, stratify=requiredTarget)
            self.clf.fit(X_train, Y_train)
            vectorized_filename = 'DataModels/ResumeModel_vector.sav'
            joblib.dump(self.tfv, vectorized_filename)
            model_filename = 'DataModels/ResumeModel.sav'
            joblib.dump(self.clf, model_filename)
            return 'Resume model is saved successfully'
        except Exception as er:
            return f"{er}"


def decider(input_data: list):
    category_list = []
    try:
        loaded_vectorizer = joblib.load('DataModels/ResumeModel_vector.sav')
        clf = joblib.load('DataModels/ResumeModel.sav')
        for i in input_data:
            predicted_data = clf.predict(loaded_vectorizer.transform([i]))
            category_list.append(predicted_data[0])
        return category_list
    except Exception as err:
        return f"Decision maker error: {err}"
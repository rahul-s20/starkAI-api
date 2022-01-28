import nltk
from app.common.makedecision.skillsList import SKILLS_DB


class SkillsExtractor:
    def __init__(self):
        try:
            self.stop_words = set(nltk.corpus.stopwords.words('english'))
        except Exception as er:
            nltk.download('stopwords')
            return "Stop was not available in the environment so downloading ..... " \
                   "Please restart the Service after download"

    def extract_skills(self, input_text: str):
        word_tokens = nltk.tokenize.word_tokenize(input_text)
        filtered_tokens = [w for w in word_tokens if w not in self.stop_words]  # remove the stop words
        filtered_tokens = [w for w in word_tokens if w.isalpha()]  # remove the punctuation
        bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2,
                                                              3)))  # generate bigrams and trigrams (such as
        # artificial intelligence)

        found_skills = set()

        for token in filtered_tokens:  # we search for each token in our skills database
            if token.lower() in SKILLS_DB:
                found_skills.add(token)

        for ngram in bigrams_trigrams:
            if ngram.lower() in SKILLS_DB:
                found_skills.add(ngram)

        if len(found_skills)> 0:
            return found_skills
        else:
            return 'No skills found'

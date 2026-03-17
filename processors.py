import spacy
from collections import Counter
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords', quiet=True)

class LanguageProcessor:
    _models = {}
    LANG_MODELS = {'fr': 'fr_core_news_sm', 'en': 'en_core_web_sm'}

    def __init__(self, lang_code='fr'):
        self.lang_code = lang_code
        self.nlp = self._get_model(lang_code)
        self.stop_words = set(stopwords.words('french' if lang_code == 'fr' else 'english'))

    def _get_model(self, lang_code):
        model_name = self.LANG_MODELS.get(lang_code)
        if model_name not in LanguageProcessor._models:
            print(f"📥 Loading NLP model: {model_name}...")
            LanguageProcessor._models[model_name] = spacy.load(model_name)
        return LanguageProcessor._models[model_name]

    def get_detailed_stats(self, text):
        doc = self.nlp(text.lower())
        lemas_filtrados = [
            token.lemma_ for token in doc 
            if token.lemma_ not in self.stop_words and token.is_alpha and len(token.text) > 1
        ]
        return {
            "total_count": len([t for t in doc if t.is_alpha]),
            "word_frequencies": Counter(lemas_filtrados)
        }
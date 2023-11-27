from .structures import Prediction

import numpy as np

import pymystem3
import nltk
from nltk.corpus import stopwords
from string import punctuation
import re
from sentence_transformers import SentenceTransformer
from gensim.models import KeyedVectors

from catboost import CatBoostClassifier
import joblib
import random
from pathlib import Path

from .config import resources_path


rubert_tiny2_model = SentenceTransformer("cointegrated/rubert-tiny2")
word2vec_model = KeyedVectors.load_word2vec_format(
    str(Path(resources_path, "ruwikiruscorpora_upos_skipgram_300_2_2018.vec.gz")), binary=False
)
le_topic = joblib.load(str(Path(resources_path, "le_topic.joblib")))
tfidf_vectorizer = joblib.load(str(Path(resources_path, "tfidf_vectorizer.joblib")))

nltk.download("stopwords")
mystem_tags_to_upos = {
    "A": "ADJ",
    "ADV": "ADV",
    "ADVPRO": "ADV",
    "ANUM": "ADJ",
    "APRO": "DET",
    "COM": "ADJ",
    "CONJ": "SCONJ",
    "INTJ": "INTJ",
    "NONLEX": "X",
    "NUM": "NUM",
    "PART": "PART",
    "PR": "ADP",
    "S": "NOUN",
    "SPRO": "PRON",
    "UNKN": "X",
    "V": "VERB",
}
russian_stopwords = stopwords.words("russian")
russian_stopwords.extend(
    ["это", "пока", "год", "везде", "пожалуйста", "добрый", "день"]
)
english_stopwords = [
    "none",
    "https",
    "id",
    "club",
    "chp",
    "files",
    "xa",
    "uploads",
    "vid",
    "com",
    "wall",
]

mystem = pymystem3.mystem.Mystem()

my_stopwords = russian_stopwords + english_stopwords


def get_tfidf_embeddings(texts):
    embeddings_tfidf = tfidf_vectorizer.transform(texts).toarray()
    return embeddings_tfidf


def get_word2vec_embeddings(document):
    zero_array = np.zeros(300)

    tokens = mystem.analyze(document)
    document_vec = list()

    for token in tokens:
        if token["text"].strip() == "":
            continue
        if not token.get("analysis"):
            continue
        lemma = token["analysis"][0]["lex"]
        part_speech = token["analysis"][0]["gr"].split(",")[0].replace("=", "")
        part_speech = re.match(r"^[A-Z]*", part_speech).group(0)
        upos = mystem_tags_to_upos[part_speech]
        word = f"{lemma}_{upos}"

        try:
            word_vec = word2vec_model[word]
        except KeyError:
            document_vec.append(zero_array)
            continue
        document_vec.append(word_vec)
    if not document_vec:
        document_vec.append(zero_array)
    return np.mean(document_vec, axis=0)


def get_many_rubert_tiny2_embeddings(texts):
    embeddings = rubert_tiny2_model.encode(texts)
    return embeddings


def preprocess_text(text):
    text = text.lower()
    text = text.replace("ё", "е")
    text = re.sub(f"[^А-Яа-я]", " ", text)
    text = " ".join(text.split())
    tokens = mystem.lemmatize(text.lower())
    new_tokens = [""]
    for token in tokens:
        if token not in my_stopwords and token != " ":
            if token.strip() not in punctuation:
                if len(token) > 2:
                    new_tokens.append(token)
    text = " ".join(new_tokens)
    return text


def get_embeddings(texts):
    tfidf_embeddings = get_tfidf_embeddings(texts)
    rubert_tiny2_embeddings = get_many_rubert_tiny2_embeddings(texts)
    rubert_word2vec_embeddings = np.array(
        [get_word2vec_embeddings(txt) for txt in texts]
    )
    # noinspection PyTypeChecker
    test_rubert_tiny2_tfidf_word2vec_embeddings = np.concatenate(
        (rubert_tiny2_embeddings, rubert_word2vec_embeddings, tfidf_embeddings),
        axis=1
    )
    return test_rubert_tiny2_tfidf_word2vec_embeddings


class TopicPredictor:
    def __init__(self, weight_path):
        self.model = CatBoostClassifier().load_model(weight_path)
        self.topic2group = joblib.load(str(Path(resources_path, "topic2group.joblib")))
        self.executors = [
            'АО ПРО ТКО', 'Александровский муниципальный округ Пермского края',
            'Бардымский муниципальный округ Пермского края', 'Город Пермь',
            'Губахинский городской округ', 'ИГЖН ПК',
            'Лысьвенский городской округ', 'Министерство здравоохранения',
            'Министерство образования', 'Министерство социального развития ПК'
        ]

    def predict(self, input_texts):
        prepared_texts = [preprocess_text(txt) for txt in input_texts]
        embeddings = get_embeddings(prepared_texts)
        output = self.model.predict(embeddings)
        topic = le_topic.inverse_transform(output)
        group = self.topic2group[topic[0]]

        return Prediction(
            topic=topic[0],
            topic_group=group,
            executor=random.choice(self.executors)
        )


model = TopicPredictor(str(Path(resources_path, "catboost_final.cbm")))

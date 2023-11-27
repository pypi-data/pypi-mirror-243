import spacy
from spacy.cli import download


download("ru_core_news_sm")


class Geography:
    def __init__(self):
        self.NER = spacy.load("ru_core_news_sm")

    def predict(self, text_message: str) -> tuple[str]:
        result: list[str] = []

        for entity in self.NER(text_message).ents:
            if entity.label_ == "LOC":
                result.append(entity.text.strip())

        return tuple(result)


geography = Geography()

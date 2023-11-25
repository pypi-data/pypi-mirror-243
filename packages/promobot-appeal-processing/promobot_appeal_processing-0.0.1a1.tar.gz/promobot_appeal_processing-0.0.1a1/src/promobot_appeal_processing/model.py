from .structures import Prediction


class Model:
    def __init__(self):
        ...

    def predict(self, text: str) -> Prediction:
        return Prediction(
            topic=text,
            topic_group=text * 2,
            executor=text * 3
        )


model = Model()

"""
Predicts the appeal topic, topic group and the executor to process the appeal based on its contents
"""

from .main import predict, predict_async, predict_many
from .structures import Prediction

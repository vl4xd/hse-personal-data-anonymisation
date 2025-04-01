import abc
import joblib

from PredictionNer import PredictionNer

class Model(abc.ABC):
    
    def __init__(self, model_joblib_path: str, model_name: str):
        self.model_joblib_path: str = model_joblib_path
        self.model_joblib: joblib = joblib.load(self.model_joblib_path)
        self.model_name: str = model_name
    
    @abc.abstractclassmethod
    def get_labels(self) -> list:
        '''Возвращает сущности, распознаваемые моделью'''
        pass
    
    @abc.abstractclassmethod
    def predict(self, text: str) -> PredictionNer:
        pass
    
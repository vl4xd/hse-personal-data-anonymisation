import abc

from classes.PredictionNer import PredictionNer


class Model(abc.ABC):
    
    
    def __init__(self, model_name: str, model_path: str):
        self.model_name: str = model_name
        self.model_path: str = model_path
    
    
    @abc.abstractclassmethod
    def get_labels(self) -> dict[int, str]:
        '''Возвращает сущности, распознаваемые моделью'''
        pass
    
    
    @abc.abstractclassmethod
    def convert_index_to_label_list(self, labels: list[int]) -> list[str]:
        pass
    
    
    @abc.abstractclassmethod
    def predict_ner(self, text: str, labels: list[str] = []) -> PredictionNer:
        pass
    
    @abc.abstractclassmethod
    def print_prediction_ner(self, prediction_ner: PredictionNer):
        pass
    
import abc
from classes.PredictionNer import PredictionNer


class Anonymizer(abc.ABC):
        
    
    @abc.abstractstaticmethod
    def anonymize(prediction_ner: PredictionNer, anon_mask: str = None) -> PredictionNer:
        pass
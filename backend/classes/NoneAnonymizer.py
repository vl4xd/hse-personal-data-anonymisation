from classes.Anonymizer import Anonymizer
from classes.PredictionNer import PredictionNer


class NoneAnonymizer(Anonymizer):
    
    @staticmethod
    def anonymize(prediction_ner: PredictionNer, anon_mask: str = None) -> PredictionNer:
        return prediction_ner


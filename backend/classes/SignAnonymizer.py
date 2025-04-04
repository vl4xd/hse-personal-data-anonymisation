from classes.Anonymizer import Anonymizer
from classes.PredictionNer import PredictionNer


class SignAnonymizer(Anonymizer):
    
    @staticmethod
    def anonymize(prediction_ner: PredictionNer, anon_mask: str = None) -> PredictionNer:
        
        result_text = ''
        left_index = 0
        for ent in prediction_ner.entities:
            result_text += prediction_ner.text[left_index:ent.start_char]
            result_text += f'<{ent.label}>'
            left_index = ent.end_char
        result_text += prediction_ner.text[left_index:len(prediction_ner.text)]
        
        prediction_ner.text = result_text
        
        return prediction_ner
import spacy

from classes.Model import Model
from classes.EntityNer import EntityNer
from classes.PredictionNer import PredictionNer

class SpacyModel(Model):
    
    
    def __init__(self,
                 model_name: str = 'SpaCy',
                 model_path: str = 'models/spacy_model'):
        
        super().__init__(model_name, model_path)
        self.model: spacy = spacy.load(self.model_path)
        
        remove_labels = ['LOC', 'ORG', 'PER'] # стандартные сущности в предобученной модели SpaCy
        model_labels = list(self.model.get_pipe('ner').labels)
        for rl in remove_labels:
            if rl in model_labels:
                model_labels.remove(rl)
                
        model_labels_dict = {}
        for i, label in enumerate(model_labels):
            model_labels_dict[i] = label
        
        self.model_labels: dict[int, str] = model_labels_dict
        
        
    def get_labels(self) -> dict[int, str]:
        return self.model_labels
    
    
    def convert_index_to_label_list(self, labels: list[int]) -> list[str]:
        result: list[str] = []
        for index in labels:
            result.append(self.model_labels[index])
        return result
    
    
    def predict_ner(self, text: str, labels: list[str] = []) -> PredictionNer:
        
        if not labels: labels = self.model_labels.values()
        
        doc = self.model(text)
        en_list = []
        for ent in doc.ents:
            
            if ent.label_ not in labels: continue
            
            entity_ner = EntityNer(ent.label_, ent.text, ent.start_char, ent.end_char)
            en_list.append(entity_ner)
        prediction_ner = PredictionNer(text, en_list)
        return prediction_ner
    
    
    def print_prediction_ner(self, prediction_ner: PredictionNer):
        result = '---\nSpacy model prediction\n---\n' + str(prediction_ner)
        print(result)
        
        
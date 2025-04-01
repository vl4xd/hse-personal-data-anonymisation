import spacy
from pathlib import Path

from Model import Model
from EntityNer import EntityNer
from PredictionNer import PredictionNer

class SpacyModel(Model):
    
    
    def __init__(self,
                 model_joblib_path: str = 'models/spacy_model.joblib',
                 model_name: str = 'SpaCy'):
        
        super().__init__(model_joblib_path, model_name)
        self.model: spacy = spacy.load(self.model_joblib)
        
    def get_labels(self):
        return list(self.model.get_pipe('ner').labels)
    
    def predict(self, text: str) -> PredictionNer:
        e = EntityNer('a', 1, 2)
        p = PredictionNer('te', [e])
        return p
        
from classes.Model import Model
from classes.SpacyModel import SpacyModel

class AvailableModels:
    
    
    __models = {
        0: ('SpaCy', SpacyModel),
        1: ('SpaCy Test', SpacyModel)
    }
    
    
    @staticmethod
    def get_index_name() -> dict[int, str]:
        result = {}
        for key, value in AvailableModels.__models.items():
            result[key] = value[0]
            
        return result
    
    
    @staticmethod
    def get_index_model() -> dict[int, Model]:
        result = {}
        for key, value in AvailableModels.__models.items():
            result[key] = value[1]
            
        return result
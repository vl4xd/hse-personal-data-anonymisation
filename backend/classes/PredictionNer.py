from classes.EntityNer import EntityNer


class PredictionNer:
    
    
    def __init__(self, text: str, entities: list[EntityNer]):
        self.text: str = text
        self.entities: list[EntityNer] = entities
        
        
    def __str__(self):
        result = f'Text: {self.text}\nEntities:\n'
        for ent in self.entities:
            result += str(ent)
        return result
from EntityNer import EntityNer

class PredictionNer:
    
    def __init__(self, text: str, entities: list[EntityNer]):
        self.text = text
        self.entities = entities
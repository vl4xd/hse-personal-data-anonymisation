
class EntityNer:
    
    def __init__(self, label: str, start_char: int, end_char: int):
        self.label = label
        self.start_char = start_char
        self.end_char = end_char
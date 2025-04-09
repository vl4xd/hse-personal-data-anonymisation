

class EntityNer:
    
    
    def __init__(self, label: str, text: str, start_char: int, end_char: int):
        self.label: str = label
        self.text: str = text
        self.start_char: int = start_char
        self.end_char: int = end_char
        
    def __str__(self):
        return f'Label: {self.label}, Text: {self.text}, Start_at: {self.start_char}, End_at: {self.end_char}\n'
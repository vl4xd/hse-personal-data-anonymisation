from classes.Anonymizer import Anonymizer
from classes.NoneAnonymizer import NoneAnonymizer
from classes.CharAnonymizer import CharAnonymizer


class AvailableAnonymizers:
    
    
    __anonymizers = {
        0: ('Без анонимизации', NoneAnonymizer),
        1: ('Замена на сигнатуру сущности', None),
        2: ('Замена на символ', CharAnonymizer)
    }
    
    
    @staticmethod
    def get_index_name() -> dict[int, str]:
        result = {}
        for key, value in AvailableAnonymizers.__anonymizers.items():
            result[key] = value[0]
            
        return result
    
    
    @staticmethod
    def get_index_anonymizer() -> dict[int, Anonymizer]:
        result = {}
        for key, value in AvailableAnonymizers.__anonymizers.items():
            result[key] = value[1]
            
        return result
from classes.Anonymizer import Anonymizer
from classes.NoneAnonymizer import NoneAnonymizer
from classes.CharAnonymizer import CharAnonymizer
from classes.SignAnonymizer import SignAnonymizer


class AvailableAnonymizers:
    
    
    __anonymizers = {
        0: ('Без анонимизации', False, NoneAnonymizer),
        1: ('Замена на сигнатуру сущности', False, SignAnonymizer),
        2: ('Замена на символ', True, CharAnonymizer)
    }
    
    
    @staticmethod
    def get_index_name() -> dict[int, (str, bool)]:
        result = {}
        for key, value in AvailableAnonymizers.__anonymizers.items():
            result[key] = {'name':value[0], 'need_mask':value[1]}
            
        return result
    
    
    @staticmethod
    def get_index_anonymizer() -> dict[int, Anonymizer]:
        result = {}
        for key, value in AvailableAnonymizers.__anonymizers.items():
            result[key] = value[2]
            
        return result
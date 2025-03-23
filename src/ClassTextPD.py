import re
import json
import numpy as np
from razdel import sentenize
from pymorphy2 import MorphAnalyzer

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import Sequential

class TextPD():
    
    
    def __init__(self, text: str):
        self.original_text: str = text
        self.edited_text: str = None
        self.sentences: list[str] = None
        self.starts: list[int] = None
        self.ends: list[int] = None
        self.tokens: list[str] = None
        self.poses: list[str] = None
        self.tokens_ids: list[int] = None
        self.poses_ids: list[int] = None
        self.tags: list[str] = None
        self.tags_ids: list[str] = None
        self.pad_tokens_ids: list[int] = None
        self.pad_poses_ids: list[int] = None
        
        self.model: Sequential = load_model('src\model.keras') # изменено для fastapi (было model.keras)
        
        self.morph = MorphAnalyzer()
        self.known_tokens_poses_tags: dict = None
        
        with open('src\known_tokens_poses_tags.json', 'r', encoding='utf-8') as file: # изменено для fastapi (было known_tokens_poses_tags.json)
            self.known_tokens_poses_tags = json.load(file)
        
        
    def fill_sentences(self):
        sentences = []
        prev_stop = None
    
        sentenize_text = sentenize(self.original_text)
        sentenize_text_len = len(list(sentenize(self.original_text))) # почему то преобразования изменяют sentenize_text, поэтому подсчитаем кол-во так
        for i, substr in enumerate(sentenize_text):
            if i == 0:
                prev_stop = substr.stop
                if substr.start > 0:
                    sentences.append(self.original_text[0:prev_stop])
                    continue
                sentences.append(self.original_text[substr.start:prev_stop])
                continue
                
            if i != 0 and i == sentenize_text_len - 1:
                sentences.append(self.original_text[prev_stop:len(self.original_text)])
                continue
            
            sentences.append(self.original_text[prev_stop:substr.stop])
            prev_stop = substr.stop
            
        self.sentences = sentences
        
        
    def fill_tokens_starts_ends(self):
        tokens_all = [] # слова по предложениям [[word1, word2]][[word1]][[word1]]
        starts_all = []
        ends_all = []
        for sentence in self.sentences:
            custom_pattern = re.compile(r"[A-Za-zА-Яа-яЁё]+|\d+|[^\w\s]|\s")
            matches = list(custom_pattern.finditer(sentence))
            starts = [match.start() for match in matches]
            ends = [match.end() for match in matches]
            matchs = [match.group() for match in matches]
            starts_all.append(starts)
            ends_all.append(ends)
            tokens_all.append(matchs)
            
        self.starts = starts_all
        self.ends = ends_all
        self.tokens = tokens_all
        
        
    def reread_starts_ends(self):
        '''Пересчитыват индексы start и end слова в контексте ондого предложения'''
        
        offset = 0 # смещение позиции относительно текста
        for i_sentence, tokens in enumerate(self.tokens):
            if not tokens: continue # проверка на пустоту токенов предложения
            for i_token, _ in enumerate(tokens):
                self.starts[i_sentence][i_token] += offset
                self.ends[i_sentence][i_token] += offset
                
            offset = self.ends[i_sentence][-1]
    
    
    def drop_spaces(self):
        spaces_list = [" ", "\u00A0", "\u202F", "\u2009", "\ufe0f", "", "\n", "\t"]
        
        tokens_clear_all = [] # слова по предложениям [[word1, word2]][[word1]][[word1]]
        starts_clear_all = []
        ends_clear_all = []
        for i_sentence, tokens in enumerate(self.tokens):
            tokens_clear = []
            starts_clear = []
            ends_clear = []
            for i_token, token in enumerate(tokens):
                if token not in spaces_list:
                    tokens_clear.append(token)
                    starts_clear.append(self.starts[i_sentence][i_token])
                    ends_clear.append(self.ends[i_sentence][i_token])
            tokens_clear_all.append(tokens_clear)
            starts_clear_all.append(starts_clear)
            ends_clear_all.append(ends_clear)
        
        self.starts = starts_clear_all
        self.ends = ends_clear_all
        self.tokens = tokens_clear_all
        
    def fill_poses(self):
        
        poses_all = []
        
        for i_sentence, tokens in enumerate(self.tokens):
            poses = []
            for i_token, token in enumerate(tokens):
                parse_token = self.morph.parse(token)
    
                if 'Name' in parse_token[0].tag:
                    poses.append('Name')
                    continue 
                if 'Surn' in parse_token[0].tag:
                    poses.append('Surn')
                    continue
                if 'Patr' in parse_token[0].tag:
                    poses.append('Patr')
                    continue
                if 'PNCT' in parse_token[0].tag:
                    poses.append('PNCT')
                    continue
                if 'NUMB' in parse_token[0].tag:
                    poses.append('NUMB')
                    continue
                if 'LATN' in parse_token[0].tag:
                    poses.append('LATN')
                    continue
        
                if parse_token[0].tag.POS:
                    poses.append(str(parse_token[0].tag.POS))
                    continue
    
                poses.append('UNKN')
            poses_all.append(poses)
        self.poses = poses_all
    
    
    def tokens_poses_to_id(self):
        tokens_ids_all = []
        poses_ids_all = []
        for i_sentence, tokens in enumerate(self.tokens):
            tokens_ids = []
            poses_ids = []
            for i_token, token in enumerate(tokens):
                if token in self.known_tokens_poses_tags['token2id']:
                    tokens_ids.append(self.known_tokens_poses_tags['token2id'][token])
                else: tokens_ids.append(self.known_tokens_poses_tags['token2id']['UNKN'])
                
                if self.poses[i_sentence][i_token] in self.known_tokens_poses_tags['pos2id']:
                    poses_ids.append(self.known_tokens_poses_tags['pos2id'][self.poses[i_sentence][i_token]])
                else: poses_ids.append(self.known_tokens_poses_tags['pos2id']['UNKN'])                
                
            tokens_ids_all.append(tokens_ids)
            poses_ids_all.append(poses_ids)

        self.tokens_ids = tokens_ids_all
        self.poses_ids = poses_ids_all

    
    def pad_tokens_poses(self):
        max_len = 50 # значение из этапа обучения модели
        
        self.pad_tokens_ids = pad_sequences(self.tokens_ids, maxlen=max_len, padding='pre', value=0)
        self.pad_poses_ids = pad_sequences(self.poses_ids, maxlen=max_len, padding='pre', value=0)
            
    
    def predict_tags_ids(self):       
        pred = self.model.predict([self.pad_tokens_ids, self.pad_poses_ids])
        pred_tags_ids = np.argmax(pred, axis=-1)
        self.tags_ids = pred_tags_ids
        
    
    def convert_tags_ids_to_tags(self):
        tags_all = []
        for tags_ids in self.tags_ids:
            tags = []
            for tag_id in tags_ids:
                if tag_id == 0: continue
                
                if str(tag_id) in self.known_tokens_poses_tags['id2tag']:
                    tags.append(self.known_tokens_poses_tags['id2tag'][f'{tag_id}'])
            tags_all.append(tags)
            
        self.tags = tags_all
    
    
    def anonymise_test(self):
        
        self.edited_text = self.original_text
        
        starts_for_anonymise = []
        ends_for_anonymise = []
        
        for i_sentence, tags in enumerate(self.tags):
            for i_tag, tag in enumerate(tags):
                if tag == 'O': continue
                starts_for_anonymise.append(self.starts[i_sentence][i_tag])
                ends_for_anonymise.append(self.ends[i_sentence][i_tag])
            
        for i_start, start in enumerate(starts_for_anonymise):
            start_indx = start
            end_indx = ends_for_anonymise[i_start]
            substr = '*' * (end_indx - start_indx)
            
            self.edited_text = self.edited_text[:start_indx] + substr + self.edited_text[end_indx:]
    
    
    def do_anonymise(self):
        self.fill_sentences()
        self.fill_tokens_starts_ends()
        self.reread_starts_ends()
        self.drop_spaces()
        self.fill_poses()
        self.tokens_poses_to_id()
        self.pad_tokens_poses()
        self.predict_tags_ids()
        self.convert_tags_ids_to_tags()
        self.anonymise_test()
    
    def __str__(self):
        result = f'\nВходной текст: {self.original_text}\n' +\
                f'Анонимизированный текст: {self.edited_text}\n' +\
                f'Разделение на предложения: {self.sentences}\n' +\
                f'Разделение на токены: {self.tokens}\n' +\
                f'Индекс слов start: {self.starts}\n' +\
                f'Инедс слов end: {self.ends}\n' +\
                f'Часть речи: {self.poses}\n' +\
                f'Индексы токенов: {self.tokens_ids}\n' +\
                f'Индексы частей речи: {self.poses_ids}\n' +\
                f'Паддинг токенов: {self.pad_tokens_ids}\n' +\
                f'Паддинг частей речи: {self.pad_poses_ids}' +\
                f'Предсказанные id тегов: {self.tags_ids}\n' +\
                f'Предсказанные теги: {self.tags}\n'
                
        return result
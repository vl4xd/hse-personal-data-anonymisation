import spacy
import joblib
from pathlib import Path

import os

print(os.getcwd())
a = joblib.load('spacy_model.joblib')
a = spacy.load(a)
print(a.get_pipe('ner').labels)

# sm = SpacyModel()
# print(sm.get_labels())

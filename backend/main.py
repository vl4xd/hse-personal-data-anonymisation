import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from classes.Model import Model
from classes.Anonymizer import Anonymizer
from classes.AvailableModels import AvailableModels
from classes.AvailableAnonymizers import AvailableAnonymizers
from classes.PredictionNer import PredictionNer


class ModelDTO(BaseModel):
    model_index: int
    

class LabelsDTO(ModelDTO):
    labels_index: list[int]
    

class AnonymizerDTO(BaseModel):
    anonymizer_index: int
    anon_mask: str | None = None


class PredictDTO(LabelsDTO, AnonymizerDTO):
    text: str


app = FastAPI()


@app.get('/models', response_class=JSONResponse)
def get_models():    
    return AvailableModels.get_index_name()


@app.post('/labels', response_class=JSONResponse)
def get_labels(modelDTO: ModelDTO):
    
    model: Model = AvailableModels.get_index_model()[modelDTO.model_index]()
    
    return model.get_labels()


@app.get('/anonymizers', response_class=JSONResponse)
def get_anonymizers():
    return AvailableAnonymizers.get_index_name()


@app.post('/predict', response_class=JSONResponse)
def get_predict(predictDTO: PredictDTO):
    
    model: Model = AvailableModels.get_index_model()[predictDTO.model_index]()
    labels = model.convert_index_to_label_list(predictDTO.labels_index)
    prediction_result: PredictionNer = model.predict_ner(predictDTO.text, labels)
    
    anonymizer: Anonymizer = AvailableAnonymizers.get_index_anonymizer()[predictDTO.anonymizer_index]
    anon_prediction_result: PredictionNer = anonymizer.anonymize(prediction_result, predictDTO.anon_mask)
    
    return anon_prediction_result


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

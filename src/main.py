import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from ClassTextPD import *


class TextDTO(BaseModel):
    text: str


app = FastAPI()


@app.get("/tags")
def get_tags():
    pass


@app.post("/anonymise_self_text")
def do_anonymise_self_text(textDTO: TextDTO):
    textPD = TextPD(textDTO.text)
    textPD.do_anonymise()
    result = {
        'original_text': textPD.original_text,
        'edited_text': textPD.edited_text,
    }
    return result

    # 'sentences': textPD.sentences,
    # 'starts': textPD.starts,
    # 'ends': textPD.ends,
    # 'poses': textPD.poses,
    # 'tokens_ids': textPD.tokens_ids,
    # 'poses_ids': textPD.poses_ids,
    # 'tags': textPD.tags,
    # 'tags_ids': textPD.tags_ids,
    # 'pad_tokens_ids': textPD.pad_tokens_ids,
    # 'pad_poses_ids': textPD.pad_poses_ids,


@app.post("/anonymise_example_text")
def do_anonymise_example_text():
    pass


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

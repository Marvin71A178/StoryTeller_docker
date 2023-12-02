from fastapi import FastAPI, Path
from typing import Optional
import Generate
from pydantic import BaseModel

class Music(BaseModel):
  name: str  

app = FastAPI()


@app.get('/')
def root():
  return {"hello": "world"}


@app.get('/gen-music')
def gen_music_api():
  return Generate.gen_music()


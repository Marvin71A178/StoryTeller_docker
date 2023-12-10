from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
import Generate
import uvicorn
import os

port = 8060

# API Model
class musicAnaLyzeModel(BaseModel):
    data: Dict[str, int]

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test API
@app.get('/')
def root() -> object:
    return {"hello": "world!"}

# Function to process music creation
async def process_music_creater(data: Dict[str, int]):
    data_len = len([i for i in data.keys()])
    if data_len == 0:
      file_name = Generate.gen_music()  # 假設 gen_music 接受 data 參數
      return file_name
    else:
      file_name = Generate.gen_music()  # 假設 gen_music 接受 data 參數
      return file_name
    
        

# Endpoint for music creation
@app.post('/music_create')
async def music_create_api(music_analyze_model: musicAnaLyzeModel, request: Request): 
    if request.headers.get('Content-Type') != 'application/json':
        raise HTTPException(status_code=422, detail="Invalid Content-Type")
    
    file_name = await process_music_creater(music_analyze_model.data)
    
    # Return the generated .wav file
    return FileResponse(file_name, media_type='audio/wav', filename=file_name)

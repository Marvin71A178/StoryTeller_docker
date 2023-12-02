from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import predict
import uvicorn
import argparse
from dotenv import load_dotenv
import os

# 加载環境變量
load_dotenv()

# 從環境變量中獲取端口號，如果不存在則默認使用8000
port = int(os.getenv("PORT", 8050))

# API Model
class MoodAnaLyzeModel(BaseModel):
  text: str  

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


async def process_emotion_ana(text):
  return predict.mood_ana_api(text)

# For Analyzing Emotion
@app.post('/emotion_analysis', response_model=int)
async def mood_analyze_api(moodAnaLyzeModel: MoodAnaLyzeModel, request: Request) -> int: 
  if request.headers.get('Content-Type') != 'application/json':
    return HTTPException(status_code=422, detail="Invalid Content-Type")
  
  if moodAnaLyzeModel.text is None or moodAnaLyzeModel.text == '':
    return HTTPException(status_code=400, detail="text is Null!")
  
  return await process_emotion_ana(moodAnaLyzeModel.text)


# 開啟伺服器
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mood analysis server')
    
    parser.add_argument(
        '--reload', '-r', action='store_true',
        help='Auto-reload server on filechanges (DEVELOPMENT)')
    args = parser.parse_args()

    reload_server = args.reload

    if reload_server:
        uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)
    else:
        uvicorn.run("app:app", host="127.0.0.1", port=port)
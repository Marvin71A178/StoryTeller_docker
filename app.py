from fastapi import FastAPI, Path, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional, Dict
from pydantic import BaseModel
import mood_analized.predict as predict 
import music_creater.Generate as Generate
import uvicorn
import psutil
import os
import asyncio

# 从环境变量中获取端口号，如果不存在则默认使用8000
port = 8050

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Models
class MoodAnalyzeModel(BaseModel):
    text: str  

class MusicAnalyzeModel(BaseModel):
    data: Dict[str, int]

# Queue for processing tasks
task_queue = asyncio.Queue()

# Test API
@app.get('/')
def root() -> object:
    return {"hello": "world!"}

# Resource usage API
@app.get("/resources")
def get_resource_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage
    }

# Emotion Analysis Processing
async def process_emotion_ana(text: str):
    return predict.mood_ana_api(text)

# Music Creation Processing
async def process_music_creater(data: Dict[str, int]):
    file_name = Generate.gen_music(data)  # Assuming gen_music accepts data parameter
    return file_name

def remove_file(file_name: str):
    """ 删除文件的函数 """
    try:
        os.remove(file_name)
    except Exception as e:
        print(f"Error while deleting file {file_name}: {e}")

# Task handler
async def task_handler():
    while True:
        task = await task_queue.get()
        await task
        task_queue.task_done()

# Start the task handler
background_tasks = BackgroundTasks()
background_tasks.add_task(task_handler)

# For Analyzing Emotion
@app.post('/emotion_analysis', response_model=int)
async def mood_analyze_api(moodAnalyzeModel: MoodAnalyzeModel): 
    if moodAnalyzeModel.text is None or moodAnalyzeModel.text == '':
        raise HTTPException(status_code=400, detail="text is Null!")

    # task = asyncio.create_task(process_emotion_ana(moodAnalyzeModel.text))
    # await task_queue.put(task)
    # return await task
    print(moodAnalyzeModel.text)
    try:
        emtion_type = await process_emotion_ana(moodAnalyzeModel.text)
    except Exception as e:
        print(e)
        emtion_type = 0
    return emtion_type

# Endpoint for music creation
@app.post('/music_create')
async def music_create_api( musicAnalyzeModel: MusicAnalyzeModel): 
    file_name = await process_music_creater(musicAnalyzeModel.data)
    
    # Return the generated .wav file
    return FileResponse(file_name, media_type='audio/wav', filename=file_name)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)

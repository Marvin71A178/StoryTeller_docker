from fastapi import FastAPI, Path, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional, Dict
from pydantic import BaseModel
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import music_creater.Generate as Generate
import uvicorn
import psutil
import os
import asyncio


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

dir_name = '/home/marvin/re_storyteller_docker/StoryTeller_docker/mood_analized/checkpoint-20000'
model_args = ClassificationArgs()
model_args.train_batch_size = 64
model_args.num_train_epochs = 3
# model_args.use_multiprocessing = False

# 讀取 ClassificationModel
model = ClassificationModel(
    'bert', 
    f"{dir_name}", # 這裡要改成訓練完成的模型資料夾路徑
    use_cuda=False, 
    cuda_device=0, 
    num_labels=6, 
    args=model_args
)

    
# Test API
@app.get('/')
def root() -> object:
    return {"hello": "world!"}


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
    
def process_music_creater(data: Dict[str, int]):
    # Here add your logic to process music creation
    file_name = Generate.gen_music(data)  # Assuming gen_music accepts data parameter
    return file_name

# def process_music_creater(content):
#     return model.predict([content])


@app.post('/emotion_analysis', response_model=int)
def mood_analyze_api(moodAnalyzeModel: MoodAnalyzeModel): 
    if moodAnalyzeModel.text is None or moodAnalyzeModel.text == '':
        raise HTTPException(status_code=400, detail="text is Null!")

    print(moodAnalyzeModel.text)
    try:
        predictions, raw_outputs = model.predict([moodAnalyzeModel.text])
    except Exception as e:
        print(e)
        predictions = 0
    return predictions

@app.post('/music_create')
def music_create_api( musicAnalyzeModel: MusicAnalyzeModel): 
    file_name = process_music_creater(musicAnalyzeModel.data)
    return FileResponse(file_name, media_type='audio/wav', filename=file_name)

if __name__ == "__main__":
    # print(model.predict(['在寒冷的冬天吃湯圓是幸福的事']))
    uvicorn.run("test:app", host="0.0.0.0", port=port , workers = 2)

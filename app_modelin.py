from flask import Flask, request, send_file
from flasgger import Swagger , swag_from
from flask_cors import CORS
from typing import Dict
from pydantic import BaseModel
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import music_creater.Generate as Generate
import psutil
import os

app = Flask(__name__)
Swagger(app)
CORS(app)

# Flask不支持Pydantic模型，您可能需要自己验证输入
# Flask also does not have dependency injection like FastAPI, so request parsing is manual

dir_name = '/home/marvin/re_storyteller_docker/StoryTeller_docker/mood_analized/checkpoint-20000'
model_args = ClassificationArgs()
model_args.train_batch_size = 64
model_args.num_train_epochs = 3

# 讀取 ClassificationModel
model = ClassificationModel(
    'bert', 
    f"{dir_name}",
    use_cuda=False, 
    cuda_device=0, 
    num_labels=6, 
    args=model_args
)

@app.route('/')
def root():
    return {"hello": "world!"}

@app.route('/resources')
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
    file_name = Generate.gen_music(data)
    return file_name

@app.route('/emotion_analysis', methods=['POST'])
def mood_analyze_api():
    data = request.json
    text = data.get('text')
    if not text:
        return {"error": "text is Null!"}, 400

    try:
        predictions, raw_outputs = model.predict([text])
    except Exception as e:
        print(e)
        predictions = 0
    return {"predictions": predictions}

@app.route('/music_create', methods=['POST'])
def music_create_api():
    data = request.json.get('data')
    file_name = process_music_creater(data)
    return send_file(file_name, mimetype='audio/wav', as_attachment=True, attachment_filename=file_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050)

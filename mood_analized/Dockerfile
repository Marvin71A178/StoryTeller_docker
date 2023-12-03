FROM storyteller123/cuda118_cudnn_pytorch210_simpletransformer:latest
COPY . /mood_analized/
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install python.dotenv
WORKDIR /mood_analized/
CMD ["python3" , "app.py"]
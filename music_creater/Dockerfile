FROM storyteller123/cuda118_cudnn_pytorch210_simpletransformer:latest
COPY . /music_creater/
WORKDIR /music_creater/
RUN apt-get update && \
    apt-get install -y fluidsynth && \
    rm -rf /var/lib/apt/lists/*
RUN pip install fastapi 
RUN pip install uvicorn
RUN pip install typing

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8060"]   
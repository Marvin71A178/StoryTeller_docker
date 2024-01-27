FROM storyteller123/cuda118_cudnn_pytorch210_simpletransformer:latest
COPY . /StoryTeller_ModelServer/
RUN pip install fastapi uvicorn psutil gdown
WORKDIR /StoryTeller_ModelServer/

RUN mkdir downloads
RUN cd downloads

RUN gdown --no-check-certificate --folder https://drive.google.com/drive/folders/1Oez7sEnwvsb7g8qYNSXQ9lAMTEFFAkv0?usp=sharing
RUN gdown https://drive.google.com/uc?id=1E0WuMMvTz_gqvitRO0IHbDaPVsly8mOD
RUN gdown https://drive.google.com/uc?id=1v9NlkxrAR0YLcfUinCtDzx84E2MliUs3
RUN unzip 'dataset.zip.zip 的副本'
RUN mv ./loss_30_params.pt ./../
RUN mv ./dataset ./../music_creater/compound-word-transformer/
RUN mv ./checkpoint-20000 ./../mood_analized/
WORKDIR /StoryTeller_ModelServer/
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8050"]
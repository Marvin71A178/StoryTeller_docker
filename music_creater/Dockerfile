FROM mcr.microsoft.com/azureml/pytorch-1.7-ubuntu18.04-py37-cpu-inference:latest
WORKDIR /home/marvin/doc_storyteller/StoryTeller_docker/music_creater
COPY . .

RUN pip3 install -r requirements.txt

CMD ["python" , "app.py"]

FROM python:3.8-slim-bullseye
WORKDIR /home/marvin/doc_storyteller/app
COPY requirements.txt ./


RUN pip3 install -r requirements.txt

COPY . .

CMD ["python" , "app.py"]

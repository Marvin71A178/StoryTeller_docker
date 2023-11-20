FROM thebloke/cuda11.8.0-ubuntu22.04-pytorch:latest
COPY . /music_creater/
WORKDIR /music_creater/


RUN python3 -m pip install --upgrade pip --no-cache-dir
RUN apt-get update && \
    apt-get install -y portaudio19-dev && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install Cython numpy
RUN pip3 install scipy cython mido pytest pyaudio pyfftw
RUN pip3 install madmom
RUN pip install subprocess.run


RUN pip3 install torch==2.1.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install torchvision==0.16.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html



RUN pip3 install -r requirements.txt
CMD ["python3" , "Generate.py"]

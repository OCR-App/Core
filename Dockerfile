FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y tesseract-ocr
RUN apt install tesseract-ocr-fas

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY LeNet5.h5 /code/
COPY cleaned_words.txt /code/
COPY . /code/

EXPOSE 8000
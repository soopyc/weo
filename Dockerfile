FROM python:3.11.5-bookworm

WORKDIR /opt/bot/

COPY ./src .

RUN [ "apt", "update" ]

RUN [ "apt", "install", "-y", "tesseract-ocr", "tesseract-ocr-eng" ] 

RUN [ "pip3", "install", "-r", "requirements.txt" ]

CMD python3 bot.py
FROM python:3

COPY ./requirements.txt /requirements.txt
COPY ./app.py /app.py

RUN pip3 install -r requirements.txt

ENTRYPOINT	["python3","app.py"]
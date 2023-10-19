FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY common/ app/utils/

COPY . .

CMD [ "python3", "run.py" ]

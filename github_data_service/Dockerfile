FROM python:3.8-slim-buster

WORKDIR /app

RUN mkdir -p ./logs

COPY github_data_service/requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY github_data_service/app .

COPY ./common ./utils/

CMD [ "python3", "run.py" ]

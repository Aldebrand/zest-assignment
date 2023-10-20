FROM python:3.8-slim-buster

WORKDIR /app

RUN mkdir -p ./logs

COPY github_data_service/requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY github_data_service/app .

COPY common/app_logging.py ./utils/app_logging.py
COPY common/redis_manager.py ./utils/redis_manager.py

CMD [ "python3", "run.py" ]

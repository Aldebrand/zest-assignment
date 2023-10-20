FROM python:3.8-slim-buster

WORKDIR /app

RUN mkdir -p ./logs

COPY auth_service/requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY auth_service/app .

COPY common/app_logging.py ./utils/app_logging.py
COPY common/db_manager.py ./utils/db_manager.py

CMD [ "python3", "run.py" ]

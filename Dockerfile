FROM python:3.10.6

WORKDIR /oti-bot

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /oti-bot/app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

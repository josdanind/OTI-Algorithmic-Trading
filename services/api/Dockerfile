FROM python:3.10.6

WORKDIR /oti-api

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# COPY . /oti-api/

EXPOSE 8082

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082", "--reload"]
FROM python:3.8.13-slim

WORKDIR /myapp

COPY requirements.txt .
COPY config/.env .
RUN apt update -y
RUN apt install git bash -y
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY . .

CMD ["python", "app.py"]

FROM python:3

WORKDIR /myapp

COPY requirements.txt .
COPY config/.env .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY . .

CMD ["python", "app.py"]

FROM python:3.8.13-slim

WORKDIR /myapp
RUN apt update -y
RUN apt install git bash -y
RUN git clone https://github.com/MiceliLanda/MicroserviceUfood.git
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r MicroserviceUfood/requirements.txt
COPY config/.env MicroserviceUfood/config/

CMD ["python", "MicroserviceUfood/app.py"]

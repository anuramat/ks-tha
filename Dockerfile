FROM python:3.10

ENV proj_path="/code"

WORKDIR ${proj_path}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

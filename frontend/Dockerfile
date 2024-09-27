FROM python:3.10-slim

RUN mkdir /frontend

WORKDIR /frontend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
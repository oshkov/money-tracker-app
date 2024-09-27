FROM python:3.10-slim

RUN mkdir /tracker_service

WORKDIR /tracker_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003"]
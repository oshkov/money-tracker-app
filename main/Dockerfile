FROM python:3.10-slim

RUN mkdir /money_tracker_app

WORKDIR /money_tracker_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
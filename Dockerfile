FROM python:3.11.4-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HOST=0.0.0.0
ENV PORT=8080

CMD uvicorn app.main:app --host $HOST --port $PORT

EXPOSE $PORT
FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install pytchat flask requests

COPY app.py /app.py

EXPOSE 10000

CMD ["python", "/app.py"]

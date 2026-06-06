FROM python:3.10-slim

# Install ca-certificates for SSL
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates && rm -rf /var/lib/apt/lists/*

RUN pip install pytchat

COPY app.py /app.py

EXPOSE 7860

CMD ["python", "/app.py"]

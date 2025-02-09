FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install prometheus-client
COPY src/consumer /app/consumer
COPY configs /app/configs
EXPOSE 8000
CMD ["python", "-m", "consumer.consumer"]

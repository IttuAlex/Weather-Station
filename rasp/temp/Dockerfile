FROM python:3.11-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install --no-cache-dir Adafruit_CircuitPython_DHT adafruit-blinka
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "dht_sensor.py"]


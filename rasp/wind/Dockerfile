FROM python:3.11-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "wind_sensor.py"]


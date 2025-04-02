import time
import requests
import adafruit_dht
import RPi.GPIO as GPIO
import board

GPIO.setmode(GPIO.BCM)
SENSOR_PIN = board.D4
LED_GREEN = 17
LED_RED = 27

gpio_pins = {LED_GREEN: GPIO.HIGH, LED_RED: GPIO.LOW}
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)

sensor = adafruit_dht.DHT11(SENSOR_PIN)

API_URL = "http://100.72.182.23:5001/save"

def read_sensor_data():
    try:
        humidity = sensor.humidity
        temperature = sensor.temperature
        
        if humidity is not None and temperature is not None:
            GPIO.output(LED_GREEN, GPIO.HIGH)
            GPIO.output(LED_RED, GPIO.LOW)
            return {
                "tip_senzor": "DHT11",
                "temperatura": temperature,
                "umiditate": humidity,
                "unitate": "C",
                "timestamp": time.time()
            }
        else:
            GPIO.output(LED_GREEN, GPIO.LOW)
            GPIO.output(LED_RED, GPIO.HIGH)
            print("Eroare la citirea senzorului.")
            return None
    except RuntimeError as e:
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(LED_RED, GPIO.HIGH)
        print(f"Eroare de citire: {e}")
        return None

try:
    while True:
        try:
            data = read_sensor_data()
            if data:
                response = requests.post(API_URL, json=data)
                if response.status_code == 201:
                    print("Date trimise cu succes la API:", response.json())
                else:
                    print("Eroare la trimiterea datelor la API:", response.text)
        except Exception as e:
            print("Eroare:", str(e))
        
        time.sleep(5)
except KeyboardInterrupt:
    print("Program oprit de utilizator.")
finally:
    GPIO.cleanup()
    sensor.exit()


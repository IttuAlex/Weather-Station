import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
TRIG = 21 
ECHO = 20 

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

diametru = 0.2  
circumferinta = 3.1416 * diametru  

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001) 
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2 
    return distance

distance_threshold = None
last_time = None

try:
    print("Asteapta valoarea de referinta")
    time.sleep(2)
    distance_threshold = measure_distance()  
    print(f"Valoare de referinta: {distance_threshold:.2f} cm")

    while True:
        dist = measure_distance()

        if dist > distance_threshold + 2:  
            current_time = time.time()
            if last_time is not None:
                period = current_time - last_time  
                viteza_vantului = circumferinta / period  
                print(f"Viteza vantului: {viteza_vantului:.2f} m/s")

            last_time = current_time  

        time.sleep(0.01)  

except KeyboardInterrupt:
    print("Masuratoare oprita")
    GPIO.cleanup()
.

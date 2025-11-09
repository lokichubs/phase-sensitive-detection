import RPi.GPIO as GPIO
import time
import sys


BUZZER_PIN = 17         
CARRIER_FREQ = 430      
DURATION_SEC = 300        

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

pwm = GPIO.PWM(BUZZER_PIN, CARRIER_FREQ)

print(f"Generating constant tone at {CARRIER_FREQ} Hz for {DURATION_SEC} seconds.")
print("Run 'data_collection.py' simultaneously to capture Dataset 2 (Unmodulated Signal + Noise).")

try:
    pwm.start(50)

    time.sleep(DURATION_SEC)
    
    print("\nTone generation finished.")

except KeyboardInterrupt:
    print("\nTone generation stopped by user.")
except Exception as e:
    print(f"\nAn error occurred: {e}", file=sys.stderr)
finally:
    # Clean up GPIO settings
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")

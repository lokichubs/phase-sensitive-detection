import RPi.GPIO as GPIO
import time
import sys

# --- Configuration ---
BUZZER_PIN = 17
CARRIER_FREQ = 430
MODULATION_FREQ = 2
DURATION_SEC = 300
LOOP_RATE = 100

# --- Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = GPIO.PWM(BUZZER_PIN, CARRIER_FREQ)

print(f"Generating {MODULATION_FREQ} Hz modulation on a {CARRIER_FREQ} Hz carrier for {DURATION_SEC} seconds.")
print("Run 'data_collection.py' simultaneously.")

start_time = time.time()

try:
    current_time = 0.0
    log_interval = 1.0 / LOOP_RATE
    modulation_period = 1.0 / MODULATION_FREQ

    pwm.start(0)  # Changed: start PWM once at 0% duty cycle instead of repeatedly start/stop
    while current_time < DURATION_SEC:
        loop_start_time = time.time()
        current_time = loop_start_time - start_time

        # Amplitude Modulation (Square Wave)
        is_on_phase = (current_time % modulation_period) < (modulation_period / 2)

        # Changed: Modulate duty cycle instead of starting/stopping PWM
        duty_cycle = 50 if is_on_phase else 0
        pwm.ChangeDutyCycle(duty_cycle)

        # Maintain Timing
        time_spent = time.time() - loop_start_time
        sleep_time = log_interval - time_spent
        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:
    print("\nSignal generation stopped by user.")
except Exception as e:
    print(f"\nAn error occurred: {e}", file=sys.stderr)
finally:
    print("Stopping PWM and cleaning up GPIO.")
    pwm.stop()  # Changed: just stop PWM once at the end
    GPIO.cleanup()
    print("Modulated signal generation complete.")

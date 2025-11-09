import Adafruit_ADS1x15
import time
import csv

adc = Adafruit_ADS1x15.ADS1115(busnum=1)
GAIN = 1
FSR = 4.096
DATA_RATE = 860  # Highest rate for ADS1115
DURATION_SEC = 10
MAX_SAMPLES = DATA_RATE * DURATION_SEC

print(f"Collecting data at {DATA_RATE} SPS for {DURATION_SEC}s...")

# Start continuous conversion mode
adc.start_adc(0, gain=GAIN, data_rate=DATA_RATE)

samples = []
start_time = time.time()

try:
    while (time.time() - start_time) < DURATION_SEC:
        value = adc.get_last_result()
        timestamp = time.time() - start_time
        voltage = (value / 32767.0) * FSR
        samples.append((timestamp, value, voltage))
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    adc.stop_adc()
    print(f"Collected {len(samples)} samples.")

# Save results to CSV at once (much faster)
file_timestamp = time.strftime("%Y-%m-%d_%H-%M", time.localtime())
filename = f"mic_data_{file_timestamp}.csv"
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["time (s)", "raw", "voltage (V)"])
    writer.writerows(samples)

print(f"Saved {len(samples)} samples to {filename}")

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import os

# --- Configuration ---
MOD_FREQ = 2                 # 2 Hz modulation frequency
CARRIER_FREQ = 430           # 430 Hz carrier frequency
DUTY_CYCLE = 0.5
T_PLOT = 10
SAMPLING_RATE = 100000

# --- Directory Setup ---
os.makedirs("data", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# --- Time Generation ---
time_s = np.linspace(0, T_PLOT, int(T_PLOT * SAMPLING_RATE), endpoint=False)

# ==========================================================
# 1. Generate Normalized 2 Hz Source Signal (Square Wave)
# ==========================================================
source_signal = signal.square(2 * np.pi * MOD_FREQ * time_s, duty=DUTY_CYCLE)
source_signal_norm = (source_signal + 1) / 2  # Normalize between 0 and 1

# --- Save to CSV ---
df_source = pd.DataFrame({
    'time (s)': time_s,
    'normalized_amplitude': source_signal_norm
})
df_source.to_csv(os.path.join("data", "dataset_1_source_signal.csv"), index=False)

# --- Plot ---
plt.figure(figsize=(10, 4))
plt.plot(time_s, source_signal_norm)
plt.title('Dataset 1: Normalized Source Signal (2 Hz Square Wave)')
plt.xlabel('Time (s)')
plt.ylabel('Normalized Amplitude (0–1)')
plt.ylim(-0.1, 1.1)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig(os.path.join("plots", "dataset_1_source_signal.png"))
plt.close()

# ==========================================================
# 2. Generate 430 Hz Carrier Signal (Square Wave)
# ==========================================================
carrier_signal = signal.square(2 * np.pi * CARRIER_FREQ * time_s, duty=DUTY_CYCLE)
carrier_signal_norm = (carrier_signal + 1) / 2  # Normalize between 0 and 1 for consistency

# --- Save to CSV ---
df_carrier = pd.DataFrame({
    'time (s)': time_s,
    'normalized_amplitude': carrier_signal_norm
})
df_carrier.to_csv(os.path.join("data", "dataset_1_carrier_signal.csv"), index=False)

# --- Plot ---
plt.figure(figsize=(10, 4))
plt.plot(time_s[:2000], carrier_signal_norm[:2000])  # Zoom in for visibility
plt.title('Dataset 1: Carrier Signal (430 Hz Square Wave)')
plt.xlabel('Time (s)')
plt.ylabel('Normalized Amplitude (0–1)')
plt.ylim(-0.1, 1.1)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig(os.path.join("plots", "dataset_1_carrier_signal.png"))
plt.close()

print("Normalized source and carrier square wave signals generated and saved successfully.")

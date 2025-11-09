import pandas as pd
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
MODULATION_FREQ = 2
INPUT_FILENAME = 'data/dataset_3_modulated_v1.csv'
OUTPUT_FILENAME = 'data/dataset_4_psd_output_v1.csv'
CUTOFF_MULTIPLIER = 5  # Filter cutoff = MODULATION_FREQ * 5

# --- LOAD DATA ---
try:
    df = pd.read_csv(INPUT_FILENAME)
    s_in = df['voltage (V)'].values
    time_s = df['time (s)'].values
    SAMPLING_RATE = 1.0 / np.mean(np.diff(time_s))
except FileNotFoundError:
    print(f"Error: Input file '{INPUT_FILENAME}' not found. Check the file name.")
    exit()

# --- RECONSTRUCT REFERENCE SIGNAL ---
modulation_period = 1.0 / MODULATION_FREQ
s_ref = np.zeros_like(s_in)
is_on_phase = (time_s % modulation_period) < (modulation_period / 2)

# Use +1/-1 for optimal mixing
s_ref[is_on_phase] = 1.0
s_ref[~is_on_phase] = -1.0

# --- PHASE-SENSITIVE DETECTION (PSD) ---

# A. Mixing (Multiplication)
s_mixed = s_in * s_ref

# B. Low-Pass Filtering (LPF)
CUTOFF_FREQ = MODULATION_FREQ * CUTOFF_MULTIPLIER
nyquist = 0.5 * SAMPLING_RATE
normal_cutoff = CUTOFF_FREQ / nyquist

if normal_cutoff >= 1:
    print("Error: Cutoff frequency too high for sampling rate.")
    exit()

b, a = scipy.signal.butter(2, normal_cutoff, btype='low', analog=False)
s_recovered = scipy.signal.lfilter(b, a, s_mixed)

# --- NORMALIZE TO [0, 1] ---
s_min, s_max = np.min(s_recovered), np.max(s_recovered)
if s_max != s_min:
    s_recovered_norm = (s_recovered - s_min) / (s_max - s_min)
else:
    s_recovered_norm = np.zeros_like(s_recovered)

# --- SAVE DATASET 4 ---
df_out = pd.DataFrame({
    'time (s)': time_s,
    'recovered_signal (V)': s_recovered,
    'recovered_signal_normalized': s_recovered_norm
})
df_out.to_csv(OUTPUT_FILENAME, index=False)
print(f"Successfully generated Dataset 4 and saved to {OUTPUT_FILENAME}")

# --- VISUALIZATION ---
plt.figure(figsize=(12, 6))
plt.plot(time_s, s_recovered_norm, color='tab:blue')
plt.title(f'Dataset 4: Recovered Signal (PSD Output, Modulation Freq: {MODULATION_FREQ} Hz)')
plt.xlabel('Time (s)')
plt.ylabel('Normalized Recovered Voltage (0–1)')
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig('plots/dataset_4_psd_output_plot_v1.png')
plt.show()

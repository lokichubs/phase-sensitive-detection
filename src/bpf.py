import os
import sys
import numpy as np
import pandas as pd
import scipy.signal
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
CARRIER_FREQ = 430.0
MODULATION_FREQ = 2.0
INPUT_FILENAME = 'data/dataset_3_modulated_v2.csv'
OUTPUT_FILENAME = 'data/dataset_5_bpf_output_v1.csv'

# Filter settings (Hz)
BPF_LOW_CUTOFF = 427.0
BPF_HIGH_CUTOFF = 433.0
LPF_CUTOFF_FREQ = MODULATION_FREQ * 5

# --- LOAD DATA ---
if not os.path.exists(INPUT_FILENAME):
    print(f"Error: Input file '{INPUT_FILENAME}' not found.")
    sys.exit(1)

df = pd.read_csv(INPUT_FILENAME)
if 'voltage (V)' not in df.columns or 'time (s)' not in df.columns:
    print("Error: expected columns 'time (s)' and 'voltage (V)' in CSV.")
    sys.exit(1)

s_in = df['voltage (V)'].values
time_s = df['time (s)'].values
if len(time_s) < 2:
    sys.exit("Error: not enough time samples.")

SAMPLING_RATE = 1.0 / np.mean(np.diff(time_s))
nyquist = 0.5 * SAMPLING_RATE
print(f"Sampling Rate: {SAMPLING_RATE:.2f} Hz, Nyquist: {nyquist:.2f} Hz")
if CARRIER_FREQ >= nyquist:
    print(f"WARNING: Carrier frequency ({CARRIER_FREQ} Hz) >= Nyquist ({nyquist:.2f} Hz). Signal may be aliased.")
else:
    print(f"Carrier Frequency: {CARRIER_FREQ} Hz (below Nyquist).")

# --- Validate bandpass cutoffs ---
low, high = float(BPF_LOW_CUTOFF), float(BPF_HIGH_CUTOFF)
if high >= nyquist:
    print(f"WARNING: BPF_HIGH_CUTOFF ({high} Hz) >= Nyquist. Clamping.")
    high = nyquist * 0.999
if low <= 0:
    print("WARNING: BPF_LOW_CUTOFF <= 0. Clamping to 1e-6.")
    low = max(low, 1e-6)
if low >= high:
    raise ValueError("BPF_LOW_CUTOFF must be smaller than BPF_HIGH_CUTOFF.")

wn_band = [low / nyquist, high / nyquist]
bpf_order = 4
sos_bpf = scipy.signal.butter(N=bpf_order, Wn=wn_band, btype='bandpass', output='sos')
s_bpf_filtered = scipy.signal.sosfiltfilt(sos_bpf, s_in)

# --- ENVELOPE DETECTION ---
s_rectified = np.abs(s_bpf_filtered)

# --- LPF to recover envelope ---
lpf_cut = float(LPF_CUTOFF_FREQ)
if lpf_cut >= nyquist:
    print(f"WARNING: LPF cutoff >= Nyquist. Clamping.")
    lpf_cut = nyquist * 0.5
wn_lpf = lpf_cut / nyquist
lpf_order = 4
sos_lpf = scipy.signal.butter(N=lpf_order, Wn=wn_lpf, btype='low', output='sos')
s_recovered = scipy.signal.sosfiltfilt(sos_lpf, s_rectified)

# --- NORMALIZE & SAVE ---
s_min, s_max = np.min(s_recovered), np.max(s_recovered)
s_recovered_norm = (s_recovered - s_min) / (s_max - s_min) if s_max != s_min else np.zeros_like(s_recovered)

df_out = pd.DataFrame({
    'time (s)': time_s,
    'recovered_signal (V)': s_recovered,
    'recovered_signal_normalized': s_recovered_norm
})
os.makedirs(os.path.dirname(OUTPUT_FILENAME) or '.', exist_ok=True)
df_out.to_csv(OUTPUT_FILENAME, index=False)
print(f"Saved Dataset 5 (BPF/Envelope) to {OUTPUT_FILENAME}")

# --- FREQUENCY DOMAIN (in dB) ---
def compute_fft_db(signal, fs):
    """Return frequency (Hz) and magnitude in dB."""
    N = len(signal)
    freqs = np.fft.rfftfreq(N, d=1/fs)
    fft_vals = np.fft.rfft(signal)
    mag = np.abs(fft_vals) / N * 2  # single-sided scaling
    mag_db = 20 * np.log10(mag + 1e-12)  # avoid log(0)
    return freqs, mag_db

freq_in, mag_in = compute_fft_db(s_in, SAMPLING_RATE)
freq_bpf, mag_bpf = compute_fft_db(s_bpf_filtered, SAMPLING_RATE)
freq_rec, mag_rec = compute_fft_db(s_recovered, SAMPLING_RATE)

plt.subplot(2, 1, 1)
plt.plot(freq_bpf, mag_bpf, color='tab:orange')
plt.title(f'BPF Output Spectrum (dB) [{low:.1f}–{high:.1f} Hz]')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True, linestyle='--', alpha=0.4)
plt.xlim(0, nyquist)

plt.subplot(2, 1, 2)
plt.plot(freq_rec, mag_rec, color='tab:red')
plt.title(f'Recovered Envelope Spectrum (dB, LPF cutoff {LPF_CUTOFF_FREQ} Hz)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True, linestyle='--', alpha=0.4)
plt.xlim(0, LPF_CUTOFF_FREQ * 10)

plt.tight_layout()
plot_path = 'plots/dataset_5_bpf_frequency_spectrum_db_v1.png'
plt.savefig(plot_path, dpi=200)
plt.show()
print(f"Saved frequency-domain (dB) plot to {plot_path}")

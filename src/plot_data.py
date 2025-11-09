import os
import pandas as pd
import matplotlib.pyplot as plt

# Define folders
data_folder = "data"
plots_folder = "plots"

# Create plots folder if it doesn't exist
os.makedirs(plots_folder, exist_ok=True)

# Loop through files in data folder
for file_name in os.listdir(data_folder):
    # Check if it's a CSV file and doesn't contain 'drive' or 'psd'
    if file_name.endswith(".csv") and "drive" not in file_name.lower() and "psd" not in file_name.lower():
        file_path = os.path.join(data_folder, file_name)

        try:
            # Read CSV
            df = pd.read_csv(file_path)

            # Normalize voltage data to range [0, 1]
            voltage = df["voltage (V)"]
            norm_voltage = (voltage - voltage.min()) / (voltage.max() - voltage.min())

            # Create plot
            plt.figure(figsize=(10, 6))
            plt.plot(df["time (s)"], norm_voltage, label="Normalized Voltage (0–1)", color='tab:blue')

            plt.title(file_name)
            plt.xlabel("Time (s)")
            plt.ylabel("Normalized Voltage (0–1)")
            plt.grid(True, linestyle="--", alpha=0.5)
            plt.legend()
            plt.tight_layout()

            # Save plot
            plot_filename = os.path.splitext(file_name)[0] + "_plot.png"
            plot_path = os.path.join(plots_folder, plot_filename)
            plt.savefig(plot_path)
            plt.close()

            print(f"Saved plot: {plot_path}")

        except Exception as e:
            print(f"Failed to process {file_name}: {e}")

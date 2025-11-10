# Phase Sensitive Detection (PSD)
A project that utilizes a Raspi-4 and microphone module to showcase the application of PSD 


## Project Overview
This project demonstrates the measurement and analysis of (PSD) as a noise filtering method using a Raspberry Pi 4,an analog microphone module, and a passive buzzer. Data is collected via an ADS1115 ADC and processed for further analysis.

## Hardware Used
- [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
- [Adafruit ADS1115 ADC](https://www.adafruit.com/product/1085)
- Analog Microphone Module
- [Passive Buzzer Module](https://www.amazon.com/Passive-Buzzer-Piezoelectric-Arduino-Raspberry/dp/B0DHGP95K4/ref=sr_1_1_pp?crid=389KLVHK8M9IU&dib=eyJ2IjoiMSJ9.WkwK2JuG0_oyZLJk32nuzMMQmdxFXb0376kz4h98OOFVcNzDvq2l6uBlRBwY_A65XfCaqRH9ciJwfix6RECxVq4phTMlHbTlkogX4zankZXnyJWfXjFUG7-0NbUa9DM-VFDsSFnOjk7Zvi8PGkY2QvU6uLOOogo-fbg5t-GXzX2uaqqxessEwlEmCGXLtOVLw7W-0U4iDgGHib2CuDKbu-0tbPXm19c-miUSKT8syuQ.cliEXetAwMtgLAe2QyVWX5nSHP3qyQBCt4iYFSDyzmo&dib_tag=se&keywords=passive%2Bbuzzer&qid=1762801815&sprefix=passive%2Bbuz%2Caps%2C180&sr=8-1&th=1)


## Usage
Make sure to run `python cd src` prior to all commands below
- To visualize the pure signal run
```bash
python signal_source.py
```

- To run the buzzer with the pure signal alone
```bash
python sound_gen_raw.py
```

- To run the modulated signal
```bash
python sound_gen_modulated.py
```

- To collect data open a **separate terminal** and run
```bash
python sound_gen_modulated.py
```

- To run psd algorithm on data
    - First replace the variables `INPUT_FILENAME` and `OUTPUT_FILENAME` in the file `psd.py` to desired file names

    - Then run the below
```bash
python psd.py
```

- To run bpf algorithm on data
    - First replace the variables `INPUT_FILENAME` and `OUTPUT_FILENAME` in the file `bpf.py` to desired file names

    - Then run the below
```bash
python bpf.py
```

## My Results
- You can find my results [here](Documentation/Report.pdf)

## References

- University of California, Berkeley. (n.d.). Phase sensitive detection and lock-in amplifiers.
Experimentation Lab. Retrieved November 9, 2025, from
https://experimentationlab.berkeley.edu/node/99

- Engineering Projects. (2021, March). What is Raspberry Pi 4? Pinout, specs, projects & datasheet.
The Engineering Projects. Retrieved from
https://www.theengineeringprojects.com/2021/03/what-is-raspberry-pi-4-pinout-specs-projects-datasheet.html

- SciPy Developers. (2024). scipy.signal.welch — Power spectral density using Welch’s method.
SciPy v1.XX documentation. Retrieved from
https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html

- DiCola, T. (2016, February 9). ADS1015 / ADS1115 | Raspberry Pi analog to digital converters.
Adafruit Learning System. Retrieved from
https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115

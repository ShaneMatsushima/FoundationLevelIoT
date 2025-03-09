import time
import Adafruit_ADS1x15

# Create an ADS1115 instance
adc = Adafruit_ADS1x15.ADS1115(busnum=1)

# Set the gain (adjust based on your sensor's output voltage range)
# GAIN = 1 for ±4.096V, GAIN = 2 for ±2.048V, GAIN = 4 for ±1.024V, etc.
GAIN = 1

# Define the analog input channel (A0, A1, A2, or A3)
CHANNEL = 1  # A0

# Conversion factor (if needed to convert raw ADC value to meaningful units)
# For example, if the sensor outputs 0-5V and GAIN = 1, the ADC range is ±4.096V.
# You may need to scale the raw value accordingly.
CONVERSION_FACTOR = (4.096 / 32767) * 3.5  # 16-bit signed value (±32767)

def read_sensor():
    """Read the raw ADC value from the specified channel."""
    raw_value = adc.read_adc(CHANNEL, gain=GAIN)
    return raw_value

def convert_to_pH(raw_value):
    """Convert the raw ADC value to voltage."""
    pH = raw_value * CONVERSION_FACTOR
    return pH

# Main loop to read and display sensor data
try:
    while True:
        raw_value = read_sensor()
        pH = convert_to_pH(raw_value)
        print(f"Raw ADC Value: {raw_value}, pH: {pH:.2f} V")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
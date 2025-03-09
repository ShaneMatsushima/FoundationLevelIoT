import blynklib
import time
import os
import glob
import Adafruit_ADS1x15

 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#define BLYNK_TEMPLATE_ID "TMPL2QxL2j53H"
#define BLYNK_TEMPLATE_NAME "IFSIPS lv1"
#define BLYNK_AUTH_TOKEN "tJeOuSoUZ9yQq4Jp4VpnSRhY6v2X7Drv"
BLYNK_AUTH = "tJeOuSoUZ9yQq4Jp4VpnSRhY6v2X7Drv"

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

TEMPERATURE_PIN = 4  # GPIO pin connected to the DHT11 sensor
# Create an ADS1115 instance
adc = Adafruit_ADS1x15.ADS1115(busnum=1)

# Set the gain (adjust based on your sensor's output voltage range)
# GAIN = 1 for ±4.096V, GAIN = 2 for ±2.048V, GAIN = 4 for ±1.024V, etc.
GAIN = 1

# Define the analog input channel (A0, A1, A2, or A3)
CHANNEL = 0  # A0

# Conversion factor (if needed to convert raw ADC value to meaningful units)
# For example, if the sensor outputs 0-5V and GAIN = 1, the ADC range is ±4.096V.
# You may need to scale the raw value accordingly.
CONVERSION_FACTOR = 4.096 / 32767  # 16-bit signed value (±32767)

# Sensor calibration parameters (adjust based on your sensor's datasheet)
VOLTAGE_DRY = 1.0  # Voltage output for dry soil
VOLTAGE_WET = 3.0  # Voltage output for wet soil
VWC_DRY = 0.0      # VWC for dry soil (0%)
VWC_WET = 1.0      # VWC for wet soil (100%)

# Function to read sensor data
def read_sensor_data():
    temperature = read_temp()
    moisture = convert_to_voltage(convert_to_voltage(read_sensor()))
    if moisture is not None and temperature is not None:
        return temperature, moisture
    else:
        print("Failed to retrieve data from sensor")
        return None, None
    
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def read_sensor():
    """Read the raw ADC value from the specified channel."""
    raw_value = adc.read_adc(CHANNEL, gain=GAIN)
    return raw_value

def convert_to_voltage(raw_value):
    """Convert the raw ADC value to voltage."""
    voltage = raw_value * CONVERSION_FACTOR
    return voltage

def convert_to_vwc(voltage):
    """Convert voltage to Volumetric Water Content (VWC)."""
    # Linear interpolation to calculate VWC
    if voltage <= VOLTAGE_DRY:
        return VWC_DRY
    elif voltage >= VOLTAGE_WET:
        return VWC_WET
    else:
        vwc = ((voltage - VOLTAGE_DRY) / (VOLTAGE_WET - VOLTAGE_DRY)) * (VWC_WET - VWC_DRY) + VWC_DRY
        return vwc

# Main loop
while True:
    # Run Blynk
   # blynk.run()

    # Read sensor data
    temperature, moisture = read_sensor_data()
    print(f"Temperature:{temperature} \t Moisture:{moisture}")

    # Send temperature to virtual pin V1
    blynk.virtual_write(0, temperature)
    # Send humidity to virtual pin V2
    blynk.virtual_write(1, moisture)

    # Wait for a few seconds before the next update
    time.sleep(5)
import blynklib
import time
import os
import glob
import spidev
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#define BLYNK_TEMPLATE_ID "TMPL2mUZa-B08"
#define BLYNK_TEMPLATE_NAME "IoT Monitoring"

BLYNK_AUTH = "1HsbA7vb5uJ-u1WyQOVQDzr7szErpMcK"

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

TEMPERATURE_PIN = 4  # GPIO pin connected to the DHT11 sensor
MOISTURE_PIN = 2
# Function to read sensor data
#TODO incorporate moisture, currently giving C and F in temperature
def read_sensor_data():
    temperature = read_temp()
    moisture = analog_to_moisture(read_analog(MOISTURE_PIN))
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

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI bus 0, device 0 (CE0)
spi.max_speed_hz = 1350000  # Set SPI speed

# Function to read analog data from MCP3008
def read_analog(channel):
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7")
    
    # MCP3008 communication protocol
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Function to convert analog value to moisture percentage
def analog_to_moisture(analog_value):
    # ME110 typically outputs higher values for dry soil and lower values for wet soil
    # Adjust these values based on your sensor's calibration
    dry_value = 1023  # Value when sensor is in dry air
    wet_value = 0     # Value when sensor is in water
    moisture_percent = 100 - ((analog_value - wet_value) / (dry_value - wet_value)) * 100
    return moisture_percent

# Main loop
while True:
    # Run Blynk
    blynk.run()

    # Read sensor data
    temperature, moisture = read_sensor_data()

    if temperature is not None and moisture is not None:
        # Send temperature to virtual pin V1
        blynk.virtual_write(1, temperature)
        # Send humidity to virtual pin V2
        blynk.virtual_write(2, moisture)

    # Wait for a few seconds before the next update
    time.sleep(5)
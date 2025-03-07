import blynklib
import time
import os
import glob
 
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

# Function to read sensor data
#TODO incorporate moisture, currently giving C and F in temperature
def read_sensor_data():
    humidity, temperature = read_temp()
    if humidity is not None and temperature is not None:
        return temperature, humidity
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
        return temp_c, temp_f


# Main loop
while True:
    # Run Blynk
    blynk.run()

    # Read sensor data
    temperature, humidity = read_sensor_data()

    if temperature is not None and humidity is not None:
        # Send temperature to virtual pin V1
        blynk.virtual_write(1, temperature)
        # Send humidity to virtual pin V2
        blynk.virtual_write(2, humidity)

    # Wait for a few seconds before the next update
    time.sleep(5)
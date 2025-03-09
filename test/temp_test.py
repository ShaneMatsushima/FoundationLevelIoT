import os
import glob
import time

# Initialize the 1-Wire interface
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Find the sensor device file
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    """Read the raw temperature data from the sensor."""
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    """Parse the raw temperature data and return the temperature in Celsius."""
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# Main loop to read temperature
try:
    while True:
        temp_c = read_temp()
        print(f"Temperature: {temp_c:.2f} °C")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
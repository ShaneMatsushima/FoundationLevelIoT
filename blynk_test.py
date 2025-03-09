import blynklib
import random
import time

# Replace with your Blynk.Console Auth Token
BLYNK_AUTH = 'tJeOuSoUZ9yQq4Jp4VpnSRhY6v2X7Drv'

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

# Function to send data to Blynk
def send_data():
    while True:
        # Generate random data (replace this with your actual sensor data)
        temperature = random.randint(20, 30)  # Example: temperature data
        humidity = random.randint(40, 60)     # Example: humidity data

        # Send data to Virtual Pins
        blynk.virtual_write(0, temperature)  # V0 for temperature
        blynk.virtual_write(1, humidity)      # V1 for humidity

        # Print the values to the console (for debugging)
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%")

        # Wait for 2 seconds before sending the next value
        time.sleep(2)

# Main loop
if __name__ == "__main__":
    try:
        # Start the Blynk connection
        while True:
            try:
                # Connect to Blynk
                blynk.run()
            except Exception as e:
                print(f"Connection error: {e}. Retrying in 5 seconds...")
                time.sleep(5)
    except KeyboardInterrupt:
        print("Program stopped.")
import requests
import time

# Replace with your Blynk Auth Token
AUTH_TOKEN = "tJeOuSoUZ9yQq4Jp4VpnSRhY6v2X7Drv"

# Blynk HTTP API URL
BLYNK_URL = f"https://blynk.cloud/external/api/update?token={AUTH_TOKEN}"

# Function to send data to Blynk
def send_to_blynk(virtual_pin, value):
    """
    Send data to a virtual pin on the Blynk dashboard.
    
    :param virtual_pin: The virtual pin number (e.g., V0, V1).
    :param value: The value to send (can be int, float, or string).
    """
    url = f"{BLYNK_URL}&{virtual_pin}={value}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Data sent to {virtual_pin}: {value}")
    else:
        print(f"Failed to send data to {virtual_pin}. Status code: {response.status_code}")

# Main loop
if __name__ == "__main__":
    try:
        while True:
            # Example: Send random data to Virtual Pin V0
            sensor_value = 42  # Replace with actual sensor data
            send_to_blynk("V1", sensor_value)

            # Wait for 2 seconds before sending the next value
            time.sleep(2)
    except KeyboardInterrupt:
        print("Program stopped.")
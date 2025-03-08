from blynklib import Blynk
import time

# Blynk Auth Token (replace with your token)
BLYNK_AUTH_TOKEN = "1HsbA7vb5uJ-u1WyQOVQDzr7szErpMcK"

# Initialize Blynk
blynk = Blynk(BLYNK_AUTH_TOKEN)

# Example variables to send to Blynk
v1 = 25.5  # Example value 1
v2 = 70.3  # Example value 2

# Function to send data to Blynk
def send_data_to_blynk():
    # Send v1 to virtual pin V1
    blynk.virtual_write(1, v1)
    # Send v2 to virtual pin V2
    blynk.virtual_write(2, v2)
    print(f"Sent to Blynk: V1 = {v1}, V2 = {v2}")

# Main loop
try:
    while True:
        # Run Blynk
        blynk.run()

        # Send data to Blynk every 5 seconds
        send_data_to_blynk()
        time.sleep(5)

        # Update v1 and v2 (for demonstration purposes)
        v1 += 1
        v2 -= 1

except KeyboardInterrupt:
    print("Exiting...")
import board
import digitalio
import adafruit_max31865
import time
import tkinter as tk

# Initialize sensor
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
sensor = adafruit_max31865.MAX31865(spi, cs, wires=3)

# Create the main window
root = tk.Tk()
root.title("Temperature Monitor")

# Create a label to display the temperature
temp_label = tk.Label(root, text="Temperature: ", font=("Arial", 36))
temp_label.pack(pady=20)

# Function to update the temperature display
def update_temp():
    try:
        temp = sensor.temperature
        tempF = temp * 9 / 5 + 32
        temp_label.config(text=f"{tempF:.1f} degF")
    except Exception as e:
        temp_label.config(text=f"Error reading temperature: {e}")

    # Schedule the next update
    root.after(1000, update_temp)  # Update every 1 second

# Initial temperature reading and display
update_temp()

# Start the main event loop
root.mainloop()

import os, sys, time, datetime
import time
import board, digitalio
import adafruit_mcp9808
import adafruit_max31865

i2c = board.I2C()
mcp = adafruit_mcp9808.MCP9808(i2c)

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
sensor = adafruit_max31865.MAX31865(spi, cs, wires=3)

if len(sys.argv) > 1:
        filename = sys.argv[1]


def append_to_file(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')

# Create the file if it doesn't exist
filename = "./Outputs/" + filename + "_" + datetime.datetime.now().strftime("%d%b%Y") +".txt"
open(filename, 'a').close()

while True:
    ambTempC = mcp.temperature
    ambTempF = ambTempC * 9 / 5 + 32
    
    chamTempC = sensor.temperature
    chamTempF = chamTempC * 9 / 5 + 32
    
    # dev = os.popen('/usr/bin/vcgencmd measure_temp')
    # s_cpuTemp = dev.read()[5:-3]
    
    text_to_append = str(chamTempF) + ", " + str(ambTempF)
    append_to_file(filename, text_to_append)
    time.sleep(5)

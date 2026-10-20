# Lab 5 - 15 second game
from machine import Pin, I2C
import time

i2c = I2C(1, sda=Pin(14), scl=Pin(15))
button = Pin(10, Pin.IN, Pin.PULL_UP)  # SW1

# Change a BCD number into a normal number
def convert(number):
    return (number // 16) * 10 + (number % 16)

# Get the time in seconds from the clock
def get_time():
    data = i2c.readfrom_mem(0x68, 0x00, 3)
    seconds = convert(data[0] & 0x7F)
    minutes = convert(data[1] & 0x7F)

    # The clock can be in 12-hour or 24-hour mode
    if data[2] & 0x40:
        hours = convert(data[2] & 0x1F)
        if hours == 12:
            hours = 0
        if data[2] & 0x20:
            hours = hours + 12
    else:
        hours = convert(data[2] & 0x3F)

    total = hours * 3600 + minutes * 60 + seconds
    return total

# Wait until SW1 is pressed and released
def wait_button():
    while button.value() == 0:
        time.sleep(0.05)
    while button.value() == 1:
        time.sleep(0.05)
    time.sleep(0.05)
    while button.value() == 0:
        time.sleep(0.05)

print("15 second guessing game")
print("Press Ctrl+C to stop")

log = open("log.txt", "a")

try:
    while True:
        print("Press SW1 to start")
        wait_button()
        start = get_time()

        print("Count 15 seconds, then press SW1 again")
        wait_button()
        end = get_time()

        difference = end - start
        if difference < 0:  # If the clock went past midnight
            difference = difference + 86400

        print("You counted", difference, "seconds")
        log.write(str(difference) + "\n")
        log.flush()

finally:
    log.close()

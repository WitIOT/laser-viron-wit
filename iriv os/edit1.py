import time
import os
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import subprocess

# Pin configuration
POWER_BUTTON = 4  # GPIO pin for the power button
BUZZER_PIN = 19   # GPIO pin for the Buzzer

# Raspberry Pi display configuration
RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(POWER_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up the power button with a pull-up resistor
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)  # Set Buzzer to off initially

# Initialize the OLED display
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

oled_init = False
timestamp = time.time()
button_press_time = None  # Track the time the button is pressed

while True:
    # Check if the button is pressed
    if GPIO.input(POWER_BUTTON) == 0:
        if button_press_time is None:
            button_press_time = time.time()  # Record the time when button press starts
            
        # Check if the button has been held for 5 seconds
        elif time.time() - button_press_time >= 5:
            if oled_init:
                try:
                    disp.clear()
                    disp.display()
                except:
                    pass

            # Turn on Buzzer for 25 milliseconds
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.025)  # Wait for 25 milliseconds
            GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off Buzzer
            os.system("sudo shutdown -h now")  # Shutdown the system
            while True:
                pass

    else:
        # Reset button press time if button is released
        button_press_time = None
        GPIO.output(BUZZER_PIN, GPIO.LOW)  # Ensure Buzzer is off when button is released

    # Display system status periodically
    if time.time() - timestamp >= 0.5:
        timestamp = time.time()
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Gather system information
        cmd = "hostname -I | cut -d' ' -f1"
        IP = subprocess.check_output(cmd, shell=True)
        cmd = "top -bn1 | grep oad | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell=True)
        cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
        temp = subprocess.check_output(cmd, shell=True)

        # Display system information on the OLED screen
        draw.text((0, 0), "IP: " + str(IP, 'utf-8'), font=font, fill=255)
        draw.text((0, 8), str(CPU, 'utf-8') + " " + str(temp, 'utf-8'), font=font, fill=255)
        draw.text((0, 16), str(MemUsage, 'utf-8'), font=font, fill=255)
        draw.text((0, 25), str(Disk, 'utf-8'), font=font, fill=255)

        # Initialize the OLED display if it hasn't been done yet
        if not oled_init:
            try:
                disp.begin()
                disp.clear()
                disp.display()
            except:
                pass
            else:
                oled_init = True

        if oled_init:
            try:
                disp.image(image.rotate(180))  # Rotate the display image 180 degrees
                disp.display()
            except:
                oled_init = False

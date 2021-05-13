import RPi.GPIO as gpio
import time
channel1 = 23
channel2 = 24

# GPIO setup
gpio.setmode(gpio.BCM)
gpio.setup(channel1, gpio.OUT)
gpio.setup(channel2, gpio.OUT)
gpio.output(channel1, gpio.HIGH)
gpio.output(channel2, gpio.HIGH)

try:
	print("channel 1 high")
	gpio.output(channel1, gpio.LOW)
	time.sleep(1)
	print("channel 1 low")
	gpio.output(channel1, gpio.HIGH)
	time.sleep(1)
	print("channel 2 high")
	gpio.output(channel2, gpio.LOW)
	time.sleep(1)
	print("channel 2 low")
	gpio.output(channel2, gpio.HIGH)
	time.sleep(1)
except KeyboardInterrupt:
	print("Keyboard interrupt")
except:
	print("some error")
finally:
	print("Clean up")
	gpio.cleanup()

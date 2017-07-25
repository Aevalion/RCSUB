import RPi.GPIO as GPIO
import dht11
import time

GPIO.setmode(GPIO.BOARD)
#setup the DHT11 on pin 7
tempreader = dht11.DHT11(pin=7)

#read from the sensor
temp = tempreader.read()

#while the readings are not valid,
#it will read again every 1s
#until the reading becomes valid
while(not temp.is_valid()):
	temp = tempreader.read()
	time.sleep(1)

#print the temperature and the humidity
#this will send them on the stdout stream
#which the sub controller will read from
print (temp.temperature)
print (temp.humidity)

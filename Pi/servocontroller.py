import time
import RPi.GPIO as GPIO

#the data pins for the servos
rservopin = 18
lservopin = 5

GPIO.setmode(GPIO.BOARD)

#setup the pins as outputs
GPIO.setup(rservopin, GPIO.OUT)
GPIO.setup(lservopin, GPIO.OUT)

#activate PWM with a frequency of 50Hz
#on the aforementioned pins
lservo = GPIO.PWM(lservopin, 50)
rservo = GPIO.PWM(rservopin, 50)

#start with the blades straight
lservo.start(3)
rservo.start(3)

#will keep looping
#saving its previous state
#while waiting for a new input at each iteration
#this avoids any conflict by queuing commands after each other
while True:
    #takes input from the user or in our case from the remotecontroller
    #the input is then stored in the variable direction as an integer
    direction = int(input(''))

    #up direction
    if(direction == 1):
        lservo.ChangeDutyCycle(8)
        rservo.ChangeDutyCycle(5)

    #down direction
    elif(direction == 2):
        lservo.ChangeDutyCycle(5)
        rservo.ChangeDutyCycle(8)

    #straight direction
    elif(direction == 0):
        lservo.ChangeDutyCycle(3)
        rservo.ChangeDutyCycle(3)

    #if the received input is none of the above
    #the sub resets to default position
    #and then the code quits the loop
    else:
	lservo.ChangeDutyCycle(3)
	rservo.ChangeDutyCycle(3)
	time.sleep(20)
	break

#clears the servo pins
lservo.stop()
rservo.stop()
GPIO.cleanup()

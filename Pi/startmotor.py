import RPi.GPIO as GPIO

#assigning pin numbers to each input
#on the L293D chip
MotorA = 37
MotorB = 38
MotorE = 40

GPIO.setmode(GPIO.BOARD)

#setting up outputs
GPIO.setup(MotorA, GPIO.OUT)
GPIO.setup(MotorB, GPIO.OUT)
GPIO.setup(MotorE, GPIO.OUT)

#turning on the motor
GPIO.output(MotorA, GPIO.LOW)
GPIO.output(MotorB, GPIO.HIGH)
GPIO.output(MotorE, GPIO.HIGH)

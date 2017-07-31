import RPi.GPIO as GPIO

#assigning pin numbers
MotorA = 37
MotorB = 38
MotorE = 40

GPIO.setmode(GPIO.BOARD)
#setting up outputs
GPIO.setup(MotorA, GPIO.OUT)
GPIO.setup(MotorB, GPIO.OUT)
GPIO.setup(MotorE, GPIO.OUT)

#stopping the motor
GPIO.output(MotorA, GPIO.LOW)
GPIO.output(MotorB, GPIO.LOW)
GPIO.output(MotorE, GPIO.LOW)

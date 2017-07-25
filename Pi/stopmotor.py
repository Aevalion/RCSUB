import RPi.GPIO as GPIO

MotorA = 37
MotorB = 38
MotorE = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MotorA, GPIO.OUT)
GPIO.setup(MotorB, GPIO.OUT)
GPIO.setup(MotorE, GPIO.OUT)

GPIO.output(MotorA, GPIO.LOW)
GPIO.output(MotorB, GPIO.LOW)
GPIO.output(MotorE, GPIO.LOW)

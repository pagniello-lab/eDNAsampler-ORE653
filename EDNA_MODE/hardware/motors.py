import RPi.GPIO as GPIO

MOTOR_PINS = {
    "main1": 22,
    "main2": 23,
    "main3": 24,
    "pres1": 25,
    "pres2": 5,
    "pres3": 6,
} # NOTE THIS CORRESPONDS TO THE GPIO PIN NAMES, NOT THE ACTUAL PIN NUMBERS

PRES_PINS_ONLY = {
    "pres1": 25,
    "pres2": 5,
    "pres3": 6,
} # NOTE THIS CORRESPONDS TO THE GPIO PIN NAMES, NOT THE ACTUAL PIN NUMBERS

SUBMERGED_PINS_ONLY = {
    "main1": 22,
    "main2": 23,
    "main3": 24,
} # NOTE THIS CORRESPONDS TO THE GPIO PIN NAMES, NOT THE ACTUAL PIN NUMBERS

GPIO.setmode(GPIO.BCM)

for pin in MOTOR_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def set_motor(name, state):
    GPIO.output(MOTOR_PINS[name], GPIO.HIGH if state else GPIO.LOW)
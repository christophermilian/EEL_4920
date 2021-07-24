import RPi.GPIO as GPIO
import time

trigPin = 16
echoPin = 18
MAX_DISTANCE = 220  # define the maximum measuring distance, unit: cm
time_out = MAX_DISTANCE * 60  # calculate timeout according to the maximum measuring distance
relayPin = 11  # define the relayPin
debounceTime = 50


def pulse_in(pin, level, time_out):  # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while GPIO.input(pin) != level:
        if (time.time() - t0) > time_out * 0.000001:
            return 0
    t0 = time.time()
    while GPIO.input(pin) == level:
        if (time.time() - t0) > time_out * 0.000001:
            return 0
    pulse_time = (time.time() - t0) * 1000000
    return pulse_time


def get_sonar():  # get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin, GPIO.HIGH)  # make trigPin output 10us HIGH level
    time.sleep(0.00001)  # 10us
    GPIO.output(trigPin, GPIO.LOW)  # make trigPin output LOW level
    ping_time = pulse_in(echoPin, GPIO.HIGH, time_out)  # read plus time of echoPin
    distance = ping_time * 340.0 / 2.0 / 10000.0  # calculate distance with sound speed 340m/s
    return distance


def setup():
    GPIO.setmode(GPIO.BOARD)  # use PHYSICAL GPIO Numbering
    GPIO.setup(trigPin, GPIO.OUT)  # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)  # set echoPin to INPUT mode
    GPIO.setup(relayPin, GPIO.OUT)  # set relayPin to OUTPUT mode


def loop():
    while True:
        time.sleep(1)
        distance = get_sonar()  # get distance
        print("The distance is : %.2f cm" % distance)
        GPIO.output(relayPin, False)  # If we don't see something, leave the relay on

        if distance < 5:
            GPIO.output(relayPin, True)  # If we see something, turn off the relay


if __name__ == '__main__':  # Program entrance
    print('Program is starting...')
    setup()
    try:
        loop()
        GPIO.output(relayPin, True)
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        GPIO.cleanup()  # release GPIO resource

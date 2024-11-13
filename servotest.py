# servo_test.py

import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setwarnings(False)

# Define the GPIO pin connected to the servo control
SERVO_PIN = 10  # Replace with your chosen GPIO pin (e.g., GPIO17)

# Set up the GPIO pin for PWM at 50Hz
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency for the SG90

# Function to set servo angle
def set_angle(angle):
    # Convert the angle to duty cycle (0°=2.5%, 180°=12.5%)
    duty_cycle = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty_cycle)

# Initialize PWM
pwm.start(0)

try:
    # Test servo at different angles
    print("Moving servo to 0°")
    set_angle(0)
    time.sleep(1)  # Wait for the servo to reach the position

    print("Moving servo to 90°")
    set_angle(90)
    time.sleep(1)

    print("Moving servo to 180°")
    set_angle(180)
    time.sleep(1)

    # Return to 90° position before stopping
    print("Returning servo to 90°")
    set_angle(90)
    time.sleep(1)

finally:
    # Clean up the GPIO and PWM
    pwm.stop()
    GPIO.cleanup()
    print("Test completed and GPIO cleaned up.")

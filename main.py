import machine
from machine import Pin
import time
import uasyncio
import socket
from mqtt import MQTTClient
import ubinascii
import math
import network
from lib.keys import *



led_pin = Pin(15, mode=Pin.OUT)
led_pin.low()

high_pin = Pin(0, mode=Pin.OUT)
high_pin.high()


class Bike_session(): # A bike session with a duration and a number of rotations

    def __init__(self):
        self.duration = 0 

        self.alive = True

        self.wheel_radius = 0.35 # wheel radius in meters. Enter your own value here.
        self.wheel_circumference = self.wheel_radius * 2 * math.pi # Wheel circumeference
        self.distance = 0 # Total distanced traveled

        self.start_time = time.time() # Start time
        self.rotations = 0

        self.sensor_pin = Pin(16, mode=Pin.IN) 
        self.sensor_pin.irq(handler=self.full_rotation_ISR, trigger=Pin.IRQ_FALLING) # Associate sensor pin with ISR. Trigger on an falling edge.

        self.switch_pin = Pin(1, mode=Pin.IN)
        self.switch_pin.irq(handler=self.unalive, trigger=Pin.IRQ_FALLING) # Assosciate button pin with ISR. Trigger on falling edge.

    def full_rotation_ISR(self, change): # ISR that increments rotations by one
        self.rotations += 1
        print(self.rotations) # For debugging

    def unalive(self, change): # ISR that ends session by removing the interrupt on pin 16.
        print("Unalive")
        print("END SESSION!")
        self.sensor_pin = None
        self.duration = time.time() - self.start_time
        self.distance = self.rotations * self.wheel_circumference
        self.alive = False
    

def do_connect():
    station = network.WLAN(network.STA_IF) # Set to station mode

    station.active(True)
    station.connect(SSID, PASSWORD) # Connect to wifi using fields in keys.py

    print("Connecting...")
    while station.isconnected() == False: # Wait for connection
        pass

    print("CONNECTED")
    led_pin.high() # Turn on LED to let us now that we're connected
    return station.ifconfig()[0] # The network configuration

def sub_cb(topic, msg): # For debugging. This function triggers when Adafruit responds to our MQTT messages.
    print(topic, msg)

def send_session(bike_session): # Function to send data to Adafruit
    try:
        do_connect()
        client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY) # Setup Adafruit credentials
        client.set_callback(sub_cb) # sub_cb triggers when messages from Adafruit arrives.
        client.connect() # Connect with credentials

        client.subscribe(AIO_SENSOR_FEED) # Subcribe to a new feed and publish our data.
        client.publish(topic=AIO_SENSOR_FEED, msg=str(bike_session.rotations))

        client.subscribe(AIO_DISTANCE_FEED)
        client.publish(topic=AIO_DISTANCE_FEED, msg=str(bike_session.distance))

        client.subscribe(AIO_DURATION_FEED)
        client.publish(topic=AIO_DURATION_FEED, msg=str(bike_session.duration))

    except KeyboardInterrupt as e:
        print("EPIC FAIL")



session = Bike_session() # When program starts, create new Bike_Session
while(True):
    if not session.alive: # Keep running for as long the Bike_Session is alive.
        send_session(session) # When Bike_Session ends, send our data
        session = None 
        break # Break the infinite loop.

print("DONE") # debugging.


 



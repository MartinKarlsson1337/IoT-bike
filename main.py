import machine
from machine import Pin
import time
import uasyncio
import socket
from mqtt import MQTTClient
import ubinascii
import math
import network
import keys



led_pin = Pin(15, mode=Pin.OUT)
led_pin.low()

high_pin = Pin(0, mode=Pin.OUT)
high_pin.high()

station = network.WLAN(network.STA_IF)

class Bike_session(): # A bike session with a duration and a number of rotations

    def __init__(self):
        self.duration = 0 

        self.alive = True

        self.wheel_radius = 0.35 # wheel radius in meters   
        self.wheel_circumference = self.wheel_radius * 2 * math.pi # Wheel circumeference
        self.distance = 0 # Total distanced traveled

        self.start_time = time.time() # Start time
        self.rotations = 0

        self.sensor_pin = Pin(16, mode=Pin.IN) 
        self.sensor_pin.irq(handler=self.full_rotation_ISR, trigger=Pin.IRQ_FALLING) # Associate sensor pin with ISR. Trigger on an falling edge.

        self.switch_pin = Pin(1, mode=Pin.IN)
        self.switch_pin.irq(handler=self.unalive, trigger=Pin.IRQ_FALLING)

    def full_rotation_ISR(self, change): # ISR that increments rotations by one
        self.rotations += 1
        print(self.rotations) # For debugging

    def unalive(self, change):
        print("Unalive")
        print("END SESSION!")
        self.sensor_pin = None
        self.duration = time.time() - self.start_time
        self.distance = self.rotations * self.wheel_circumference
        self.alive = False
    

def do_connect():
    station = network.WLAN(network.STA_IF)

    station.active(True)
    station.connect(keys.SSID, keys.PASSWORD)

    print("Connecting...")
    while station.isconnected() == False:
        pass

    print("CONNECTED")
    led_pin.high()
    return station.ifconfig()[0]

def sub_cb(topic, msg):
    print(topic, msg)

def send_session(bike_session):
    try:
        do_connect()
        client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)
        client.set_callback(sub_cb)
        client.connect()

        client.subscribe(AIO_SENSOR_FEED)
        client.publish(topic=AIO_SENSOR_FEED, msg=str(bike_session.rotations))

        client.subscribe(AIO_DISTANCE_FEED)
        client.publish(topic=AIO_DISTANCE_FEED, msg=str(bike_session.distance))

        client.subscribe(AIO_DURATION_FEED)
        client.publish(topic=AIO_DURATION_FEED, msg=str(bike_session.duration))

    except KeyboardInterrupt as e:
        print("EPIC FAIL")



session = Bike_session()
while(True):
    if not session.alive:
        send_session(session)
        session = None
        break

print("DONE")


 



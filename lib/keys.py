import ubinascii
import machine

SSID = "Wifi-name"
PASSWORD = "Wifi-password"

AIO_USER = "Your Adafruit account name"
AIO_KEY = "Your Adafruit key"
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883

AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_SENSOR_FEED = "Path to your rotations feed"
AIO_DISTANCE_FEED = "Path to your distance feed"
AIO_DURATION_FEED = "Path to your duration feed"

Author: Martin Karlsson
ID: mk225jy
# Tutorial on how to make your bike your first IoT project
This project is about creating a simple IoT solution for measuring how far you travel with your bike.
The device created in this project will be able to count the number of rotations a bike wheel makes, and 
with that data, calculate a distance. 

The project is relatively short and easy to complete. The time it takes to complete this project depends on the 
shipping time of the required hardware. Following this tutorial, the project should only take about 2-3 hours to complete. 

# Objective
The objective of this project is to measure how far you travel with you travel with your bike. 

The data is collected by a microcontroller attached to your bike, which sends data via Wifi to a dashboard on Adafruit 
using the MQTT protocol. 

# Material
For this specific project I used the Raspberry Pi Pico WH. It is suitable for this project since it is also equipped with a 2.4GHz wireless interface. If you would like to read more about the RPi Pico WH, you can have a look at the [datasheet](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf).

To count the number of rotations your bike wheel makes, the [TLV49645 SIP-3](https://www.electrokit.com/uploads/productfile/41015/2343219.pdf) Hall-effect sensor is used. To use the sensor you also need a magnet. The sensor outputs a digital signal. 

To power the microcontroller you also need some sort of battery pack. The microcontroller needs at least 1.8V to power (5.5V maximum). I used a small battery pack with 2 AAA batteries.

Furthermore, you need a breadboard, some jumpers to connect sensors, and a micro-USB cable. You will need at least 3 male-to-female connectors that are at least 30 cm. They will be used to connect the sensor to the breadboard. If they are to short, it will be hard to position the sensor correctly. 

INSERT BILL OF MATERIALS AND PRICES
# Computer Setup
In this project [Visual Studio Code](https://code.visualstudio.com/) was used. To upload code to the Pico WH, the [pymakr](https://github.com/pycom/pymakr-vsc/blob/HEAD/GET_STARTED.md) extension was used.

Your OS should not matter in this project, so any OS is fine. 

## Step-by-step

1. Install [Python](https://www.python.org/downloads/) if you don't already have it.
2. Install [VSCode](https://code.visualstudio.com/) if you don't already have it.
3. Get the [PyMakr](https://github.com/pycom/pymakr-vsc/blob/HEAD/GET_STARTED.md) extension in VSCode.
4. Update the firmware on the microcontroller. If Raspberry Pi Pico is used, follow these steps:    
    1. Download the [MicroPython firmware](https://micropython.org/download/rp2-pico-w/). Use the one under "Releases" and not "Nightly Builds".
    2. Connect the Micro-USB cable to the Pico.
    3. Insert the other end of the cable to your computer, while holding down the BOOTSEL button of the RPi Pico. 
    4. A new device called RPI-RP2 should now show up in your file system. Move the file from step 1 into it's storage. 
    5. Wait. The board should automatically disconnect and then reconnect to your computer. This might take a while sometimes.
5. The setup is done! You're ready to code!

# Putting everything together
This diagram shows how to connect everything. The hall effect sensor might be a bit tricky to connect. Make sure that you connect it using wires, and not directly to the breadboard. This ensures that we can easily position the sensor correctly. 
![alt text](img/schematic.png)

The green LED seen in the schematic is not a requirement for the device to function properly. Its purpose is to indicate that a Wi-Fi connection has been established, and that it is sending data via that connection.

# Platform
I used Adafruit for this project. It is a free and easy to use. It is capable of creating simple visualizations for your data. 

First, create an [Adafruit IO](https://io.adafruit.com/) account. Then, create three new feeds: rotations, distance and duration. If you're having trouble creating feeds, there's a guide [here](https://learn.adafruit.com/adafruit-io-basics-feeds).

# Code
The screenshot below shows how to structure your project. 
![alt text](img/fileStructure.png)

The **lib** folder holds all essential libraries for this project. 
# Transmitting data

# Presenting data

# Final thoughts and design



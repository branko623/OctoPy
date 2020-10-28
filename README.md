Raw RGB Python to OctoWS2811 on Teensy4
======================

I wrote this code as a solution to send raw RGB data calculated in cython/python to a dedicated Teensy4 running OctoWS2811 via USB cable.<br>

You can run the python code on any Linux system, including Raspberry Pi's. Operating systems such as linux are not optimized to drive timing-critical applications like NeoPixels. The easiest way to control NeoPixels with Python is to run the code on a system like Linux and send that data to a microcontroller more capable of always meeting the critical timing requirements. One such (over)capable microcontroller is the Teensy. The latest iteration, 4, can drive up to 16 channels, with pins configurable by the user.  <br>

This code is written specifically for the Teensy4, but other Teensy's can be used if the pinList configuration is ignored. <br>

Upload rcv/rcv.ino to a Teensy and connect to your system with a USB cable.<br>

To use this code, configure both files with pin numbers, strip lengths, and other settings. 

Usage
-------------------
```python
from OctoWS2811 import OctoWS2811 
strips = [50,49,38,40,40,45,45,50,48] #configure strip lengths
display = OctoWS2811(strips,usb='/dev/serial/by-id/usb-Teensyduino_USB_Serial_0000000-0000',fps_show=True)
```

Then send display data in RGB format in one large bytearray()(configure color order in rcv.ino, but send data in order R-G-B) 
```python
display.write(some_big_bytearray)
```

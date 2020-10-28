import math
import serial
import time
from struct import pack

class OctoWS2811:
    '''Send raw pixel data to a device that is loaded with 
    the rcv.ino code in this repository via USB:  

    strips: Pass a list with the sizes of each strip in order
        that is defined on the microchip
    usb: pass a usb port e.g. "/dev/serial/by-id/usb-Teensyduino_USB_Serial_0000000-0000"
    fps_show: print fps every second

    '''
    def __init__(self, strips, usb = "/dev/serial0",  fps_show = False):
    
        self.usb = usb
        
        self.largest_strip = 0
        self.draw_time = time.time()
        
        self.fps_show = fps_show
        self.frametime = time.time()
        self.fps = 0
        self.trigger = 1 # 1 = allow send, 0 = wait
        self.strips = strips
        
        self.config = {}

        for i in range(0,len(strips)):
            self.config[i] = {}
            self.config[i]['size'] = strips[i]
            self.config[i]['bpp'] = 3 #OctoWS2811 only supports 3
        self.__setup()

    #one time setup run, create the buffer
    def __setup(self):
        self.size = 0 #total pixels among all strips
        self.port = serial.Serial(self.usb, timeout=0)  

        mark = 0
        for c in self.config.values():
            
            if c['size'] > 0:
                self.size += c['size']
                
                c['data_offset'] = mark
                c['data_bytes'] = c['size'] *c['bpp']
                mark += c['data_bytes'] 
                
                if self.largest_strip < c['size']:
                    self.largest_strip = c['size']
                    
    def _get(self):
        r = 0
        while self.trigger == 0:
            r = self.port.read()
            if r == b'x':
                self.trigger = 1

    def write(self,data):
        ''' pass raw rgb data in one bytearray''' 

        #fps code
        if self.fps_show:
            now = time.time()
            self.fps += 1
            if now > math.ceil(self.frametime):
                print ("FPS: %s" %self.fps)
                self.fps = 0
            self.frametime = now
                
        self.buffer = bytearray(b'DATA') #clear bytearray
        
        if isinstance(data,bytearray): # one bytearray 

            for c in self.config.values(): 
                self.buffer.extend(pack(">H",c['size'])) 
                self.buffer += data[c['data_offset']:c['data_offset']+c['data_bytes']]
                
        else:
            raise ValueError ("Pass one bytearray to write())")
        
        self._get() #wait for trigger 
        
        self.port.write(self.buffer)

        self.trigger = 0 #reset trigger

if __name__ == "__main__":
    print ("TEST SCRIPT")
    import random
    strips = [34,27,32,34,20,27,20,27,21]
    display = OctoWS2811(strips,usb='/dev/serial/by-id/usb-Teensyduino_USB_Serial_8046140-if00',fps_show=True)

    tot = sum(strips)
    bpp = 3
    data = bytearray([0 for _ in range(tot*bpp)])

    pal = [0,0,150],[150,0,0],[0,150,0]

    while True:
        x = random.randint(0,400)
        if len(data) > tot*bpp-bpp:
            data = data[bpp:]
        if x<3:
            data.extend(pal[x])
        else:
            data.extend([0,0,0])

        display.write(data)


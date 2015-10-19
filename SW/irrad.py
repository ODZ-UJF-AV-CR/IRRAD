#!/usr/bin/python

#uncomment for debbug purposes
#import logging
#logging.basicConfig(level=logging.DEBUG) 

import sys
import time
from pymlab import config

XSMM = 641
YSMM = 642
ZSMM = 32256


class axis:
    def __init__(self, SPI_CS, Direction):
        """ One axis of robot """
        self.CS = SPI_CS
        self.Dir = Direction
        self.Reset()

    def Reset(self):
        """ Reset Axis an set default parameters for H-bridge """
        spi.SPI_write(self.CS, [0xC0])      # reset
        spi.SPI_write(self.CS, [0x14])      # Stall Treshold setup
        spi.SPI_write(self.CS, [0x7F])  
        spi.SPI_write(self.CS, [0x14])      # Over Current Treshold setup 
        spi.SPI_write(self.CS, [0x0F])  
        #spi.SPI_write(self.CS, [0x15])      # Full Step speed 
        #spi.SPI_write(self.CS, [0x00])
        #spi.SPI_write(self.CS, [0x30]) 
        #spi.SPI_write(self.CS, [0x0A])      # KVAL_RUN
        #spi.SPI_write(self.CS, [0x50])
      
    def MaxSpeed(self, speed):
        """ Setup of maximum speed """
        spi.SPI_write(self.CS, [0x07])       # Max Speed setup 
        spi.SPI_write(self.CS, [0x00])
        spi.SPI_write(self.CS, [speed])  

    def ReleaseSW(self):
        """ Go away from Limit Switch """
        while self.ReadStatusBit(2) == 1:           # is Limit Switch ON ?
            spi.SPI_write(self.CS, [0x92 | (~self.Dir & 1)])     # release SW 
            while self.IsBusy():
                pass
            spi.SPI_write(self.CS, [0x40 | (~self.Dir & 1)])       # move 0x2000 steps away
            spi.SPI_write(self.CS, [0x00])
            spi.SPI_write(self.CS, [0x20])
            spi.SPI_write(self.CS, [0x00])
            while self.IsBusy():
                pass
 
    def GoZero(self, speed):
        """ Go to Zero position """
        self.ReleaseSW()

        spi.SPI_write(self.CS, [0x82 | (self.Dir & 1)])       # Go to Zero
        spi.SPI_write(self.CS, [0x00])
        spi.SPI_write(self.CS, [speed])  
        while self.IsBusy():
            pass
        time.sleep(0.3)
        self.ReleaseSW()

    def Move(self, steps):
        """ Move some steps from current position """
        if steps > 0:                                          # look for direction
            spi.SPI_write(self.CS, [0x40 | (~self.Dir & 1)])       
        else:
            spi.SPI_write(self.CS, [0x40 | (self.Dir & 1)]) 
        steps = int(abs(steps))     
        spi.SPI_write(self.CS, [(steps >> 16) & 0xFF])
        spi.SPI_write(self.CS, [(steps >> 8) & 0xFF])
        spi.SPI_write(self.CS, [steps & 0xFF])

    def MoveWait(self, steps):
        self.Move(steps)
        while self.IsBusy():
            pass

    def Float(self):
        """ switch H-bridge to High impedance state """
        spi.SPI_write(self.CS, [0xA0])

    def ReadStatusBit(self, bit):
        """ Report given status bit """
        try:
            spi.SPI_write(self.CS, [0x39])   # Read from address 0x19 (STATUS)
            spi.SPI_write(self.CS, [0x00])
            data = spi.SPI_read(1)                  # 1st byte
            spi.SPI_write(self.CS, [0x00])
            data.extend(spi.SPI_read(1))            # 2nd byte
            if bit > 7:                                   # extract requested bit
                OutputBit = (data[0] >> (bit - 8)) & 1
            else:
                OutputBit = (data[1] >> bit) & 1        
            return OutputBit
        except IOError(): ### TODO
            spi.SPI_write(self.CS, [0x39])   # Read from address 0x19 (STATUS)
            spi.SPI_write(self.CS, [0x00])
            data = spi.SPI_read(1)                  # 1st byte
            spi.SPI_write(self.CS, [0x00])
            data.extend(spi.SPI_read(1))            # 2nd byte
            if bit > 7:                                   # extract requested bit
                OutputBit = (data[0] >> (bit - 8)) & 1
            else:
                OutputBit = (data[1] >> bit) & 1        
            return OutputBit
        finally:
            pass

    
    def IsBusy(self):
        """ Return True if tehre are motion """
        if self.ReadStatusBit(1) == 1:
            return False
        else:
            return True


cfg = config.Config(
    i2c = {
        "port": 8,
    },

    bus = [
        { "name":"spi", "type":"i2cspi"},
    ],
)

cfg.initialize()

print "Irradiation unit. \r\n"

spi = cfg.get_device("spi")



try:

    while True:
        print "SPI configuration.."
        spi.SPI_config(spi.I2CSPI_MSB_FIRST| spi.I2CSPI_MODE_CLK_IDLE_HIGH_DATA_EDGE_TRAILING| spi.I2CSPI_CLK_461kHz)

        print "Robot inicialization"
        X = axis(spi.I2CSPI_SS1, 0)
        Y = axis(spi.I2CSPI_SS0, 1)
        Z = axis(spi.I2CSPI_SS2, 1)
        X.MaxSpeed(60)
        Y.MaxSpeed(60)
        Z.MaxSpeed(38)
        
        Z.GoZero(100)
        Z.Move(100000)
        X.GoZero(20)
        Y.GoZero(20)

        time.sleep(1)

        X.Move(30*XSMM)
        Y.Move(50*YSMM)
        Z.MoveWait(58*ZSMM)
        X.Move(50*XSMM)
            
        print "Robot is running"

        for y in range(5):
            for x in range(5):
                Z.MoveWait(5*ZSMM)
                time.sleep(1)
                Z.MoveWait(-5*ZSMM)
                if x < 4:
                    X.MoveWait(8*XSMM)
            Y.MoveWait(8*YSMM)
            for x in range(5):
                Z.MoveWait(5*ZSMM)
                time.sleep(1)
                Z.MoveWait(-5*ZSMM)
                if x < 4:
                    X.MoveWait(-8*XSMM)
            Y.MoveWait(8*YSMM)

        X.MoveWait(-20*XSMM)
        Z.MoveWait(-30*ZSMM)
        X.Float()
        Y.Float()
        Z.Float()
            

        '''
        while True:
            print X.ReadStatusBit(2)
            time.sleep(1)
        '''

finally:
    print "stop"

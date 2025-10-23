#!/usr/bin/env python3
# coding: utf-8
import smbus
import time,random
import math

PI5Car_I2CADDR = 0x2B
class Raspbot():
    # init
    def get_i2c_device(self, address, i2c_bus):
        self._addr = address
        if i2c_bus is None:
            return smbus.SMBus(1)
        else:
            return smbus.SMBus(i2c_bus)

    def __init__(self):
        # Create I2C device.
        self._device = self.get_i2c_device(PI5Car_I2CADDR, 1)

    # core smbus functions
    def write_u8(self, reg, data):
        try:
            self._device.write_byte_data(self._addr, reg, data)
        except:
            print ('write_u8 I2C error')

    def write_reg(self, reg):
        try:
            self._device.write_byte(self._addr, reg)
        except:
            print ('write_u8 I2C error')

    def write_array(self, reg, data):
        try:
            # self._device.write_block_data(self._addr, reg, data)
            self._device.write_i2c_block_data(self._addr, reg, data)
        except:
            print ('write_array I2C error')

    def read_data_byte(self):
        try:
            buf = self._device.write_byte(self._addr)
            return buf
        except:
            print ('read_u8 I2C error')

    def read_data_array(self,reg,len):
        try:
            buf = self._device.read_i2c_block_data(self._addr,reg,len)
            return buf
        except:
            print ('read_u8 I2C error')

    # control functions
    def Ctrl_Car(self, motor_id, motor_dir,motor_speed):
        try:
            if(motor_dir !=1)and(motor_dir != 0):  
                motor_dir = 0
            if(motor_speed>255):
                motor_speed = 255
            elif(motor_speed<0):
                motor_speed = 0

            reg = 0x01
            data = [motor_id, motor_dir, motor_speed]
            self.write_array(reg, data)
        except:
            print ('Ctrl_Car I2C error')

    def Ctrl_Camera_Servo(self, id, angle):
        try:
            reg = 0x02
            data = [id, angle]
            if angle < 0:
                angle = 0
            elif angle > 180:
                angle = 180
            if(id==2 and angle > 100):angle = 100
            self.write_array(reg, data)
        except:
            print ('Ctrl_Camera_Servo I2C error')

    def Ctrl_Headlights_Color_All(self, state, color):
        try:
            reg = 0x03
            data = [state, color]
            if state < 0:
                state = 0
            elif state > 1:
                state = 1
            self.write_array(reg, data)
        except:
            print ('Ctrl_Headlights_All I2C error')

    def Ctrl_Headlights_Color_Alone(self, number,state, color):
        try:
            reg = 0x04
            data = [number,state, color]
            if state < 0:
                state = 0
            elif state > 1:
                state = 1
            self.write_array(reg, data)
        except:
            print ('Ctrl_Headlights_Alone I2C error')

    def Ctrl_Headlights_brightness_ALL(self, R, G, B):
        try:
            reg = 0x08
            data = [R,G,B]
            if R >255:
                R =255
            if G > 255:
                G = 255
            if B >255:
                B=255
            self.write_array(reg, data)
        except:
            print ('Ctrl_Headlights I2C error') 

    def Ctrl_Headlights_brightness_Alone(self, number, R, G, B):
        try:
            reg = 0x09
            data = [number,R,G,B]
            if R >255:
                R =255
            if G > 255:
                G = 255
            if B >255:
                B=255
            self.write_array(reg, data)
        except:
            print ('Ctrl_Headlights_Alone I2C error') 

    def Ctrl_IR_Switch(self, state):
        try:
            reg = 0x05
            data = [state]
            if state < 0:
                state = 0
            elif state > 1:
                state = 1
            self.write_array(reg, data)
        except:
            print ('Ctrl_IR_Switch I2C error')

    def Ctrl_BEEP_Switch(self, state):
        try:
            reg = 0x06
            data = [state]
            if state < 0:
                state = 0
            elif state > 1:
                state = 1
            self.write_array(reg, data)
        except:
            print ('Ctrl_BEEP_Switch I2C error')

    def Ctrl_Ulatist_Switch(self, state):
        try:
            reg = 0x07
            data = [state]
            if state < 0:
                state = 0
            elif state > 1:
                state = 1
            self.write_array(reg, data)
        except:
            print ('Ctrl_Ulatist_Switch I2C error')

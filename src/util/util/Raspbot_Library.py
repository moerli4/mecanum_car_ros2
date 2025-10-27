#!/usr/bin/env python3

import smbus
import warnings

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
        """control the cars motors

        Args:
            motor_id (int): id of the motor to control 0, 1, 2, 3 for L1, L2, R1, R2 respectively
            motor_dir (int): 0 for forwards, 1 for backwards
            motor_speed (int): speed value, [0, 255]
        """
        try:
            # assert types
            if not all(isinstance(v, int) for v in (motor_id, motor_dir, motor_speed)):
                raise TypeError("motor_id, motor_dir and motor_speed must be ints")

            # clamp to valid value ranges
            if motor_speed < 0 :
                warnings.warn("motor_speed must be in [0,255], clamping to 0")
                motor_speed = 0
            elif motor_speed > 255:  
                warnings.warn("motor_speed must be in [0,255], clamping to 255")
                motor_speed = 255

            # check other values for validity
            if not motor_id in (0,1,2,3):
                raise ValueError("motor_id must be one of {0,1,2,3}")
            if not motor_dir in (0,1):
                raise ValueError("motor_dir must be one of {0,1}")

            # write to reg
            reg = 0x01
            data = [motor_id, motor_dir, motor_speed]
            self.write_array(reg, data)

        except Exception as e:
            warnings.warn(f"Ctrl_Car I2C error: {e}")

    def Ctrl_Camera_Servo(self, id, angle):
        """control camera servo position

        Args:
            id (int): id of servo motor, {1,2}
            angle (int): angle at which to set the servo in degrees, [0,180]
        """
        try:
            # assert types
            if not all(isinstance(v, int) for v in (id, angle)):
                raise TypeError("id and angle must be ints")

            # clamp angle
            if angle < 0:
                warnings.warn("angle must be in [0,180]; clamping to 0")
                angle = 0
            elif angle > 180:
                warnings.warn("angle must be in [0,180]; clamping to 180")
                angle = 180

            # per-servo limit
            if id == 2 and angle > 100:
                warnings.warn("servo 2 max angle is 100; clamping to 100")
                angle = 100

            # validate id
            if id not in (1, 2):
                raise ValueError("id must be one of {1,2}")

            # write to reg
            reg = 0x02
            data = [id, angle]
            self.write_array(reg, data)
        except Exception as e:
            warnings.warn(f"Ctrl_Camera_Servo I2C error: {e}")

    def Ctrl_Headlights_ALL(self, R, G, B):
        """control all headlight LEDs color and intensity precisely and simultaneously

        Args:
            R (int): intensity of red, [0,255]
            G (int): intensity of green, [0,255]
            B (int): intensity of blue, [0,255]
        """
        try:
            # assert types
            if not all(isinstance(v, int) for v in (R, G, B)):
                raise TypeError("R, G and B must be ints")

            # clamp RGB
            if R < 0:
                warnings.warn("R must be in [0,255]; clamping to 0")
                R = 0
            elif R > 255:
                warnings.warn("R must be in [0,255]; clamping to 255")
                R = 255

            if G < 0:
                warnings.warn("G must be in [0,255]; clamping to 0")
                G = 0
            elif G > 255:
                warnings.warn("G must be in [0,255]; clamping to 255")
                G = 255

            if B < 0:
                warnings.warn("B must be in [0,255]; clamping to 0")
                B = 0
            elif B > 255:
                warnings.warn("B must be in [0,255]; clamping to 255")
                B = 255

            # write to reg
            reg = 0x08
            data = [R, G, B]
            self.write_array(reg, data)
        except Exception as e:
            warnings.warn(f"Ctrl_Headlights_ALL I2C error: {e}")

    def Ctrl_Headlights_ID(self, number, R, G, B):
        """control headlight LEDs color and intensity individually and precisely

        Args:
            number (int): id of the headlight LED, [1,14]
            R (int): intensity of red, [0,255]
            G (int): intensity of green, [0,255]
            B (int): intensity of blue, [0,255]
        """
        try:
            # assert types
            if not all(isinstance(v, int) for v in (number, R, G, B)):
                raise TypeError("number, R, G and B must be ints")

            # validate number
            if number not in range(1, 15):
                raise ValueError("number must be in [1,14]")

            # clamp RGB (same warnings as above)
            if R < 0:
                warnings.warn("R must be in [0,255]; clamping to 0")
                R = 0
            elif R > 255:
                warnings.warn("R must be in [0,255]; clamping to 255")
                R = 255

            if G < 0:
                warnings.warn("G must be in [0,255]; clamping to 0")
                G = 0
            elif G > 255:
                warnings.warn("G must be in [0,255]; clamping to 255")
                G = 255

            if B < 0:
                warnings.warn("B must be in [0,255]; clamping to 0")
                B = 0
            elif B > 255:
                warnings.warn("B must be in [0,255]; clamping to 255")
                B = 255

            # write to reg
            reg = 0x09
            data = [number, R, G, B]
            self.write_array(reg, data)
        except Exception as e:
            warnings.warn(f"Ctrl_Headlights_ID I2C error: {e}")

    def Ctrl_IR_Remote_Sensor(self, state):
        """turn off or on infrared sensor for remote control data

        Args:
            state (int): 0 for OFF, 1 for ON
        """
        try:
            # assert type
            if not isinstance(state, int):
                raise TypeError("state must be int")
            
            # validate state
            if state not in (0,1):
                raise ValueError("state must be in {0,1}")

            # write to reg
            reg = 0x05
            data = [state]
            self.write_array(reg, data)
        except Exception as e:
            warnings.warn(f"Ctrl_IR_Remote_Sensor I2C error: {e}")

    def Ctrl_BEEP_Switch(self, state):
        """enable or disable the beep/buzzer

        Args:
            state (int): 0 for OFF, 1 for ON
        """
        try:
            # assert type
            if not isinstance(state, int):
                raise TypeError("state must be int")

            # validate state
            if state not in (0,1):
                raise ValueError("state must be in {0,1}")

            # write to reg
            reg = 0x06
            data = [state]
            self.write_array(reg, data)
        except Exception as e:
            warnings.warn(f"Ctrl_BEEP_Switch I2C error: {e}")

    def Ctrl_Ultrasound_Sensor(self, state):
        """enable or disable the ultrasound distance sensor

        Args:
            state (int): 0 for OFF, 1 for ON
        """
        try:
            # assert type
            if not isinstance(state, int):
                raise TypeError("state must be int")

            # validate state
            if state not in (0,1):
                raise ValueError("state must be in {0,1}")

            # write to reg
            reg = 0x07
            data = [state]
            self.write_array(reg, data)
        except Exception as e:
            warnings.warn(f"Ctrl_Ultrasonic_Switch I2C error: {e}")
        
    # functions for reading sensors
    def Read_IR_Remote_Sensor(self):
        """read infrared sensor data for remote control sensor

        Returns:
            list: IR sensor data
        """
        try:
            reg = 0x0c
            return self.read_data_array(reg,1)
        except Exception as e:
            warnings.warn(f"Ctrl_IR_Remote_Sensor I2C error: {e}")
            return []

    def Read_Ultrasound_Sensor(self):
        """read ultrasound data
        
        Returns:
            list: ultrasound distance in mm
        """
        try:
            diss_H = self.read_data_array(0x1b,1)[0]
            diss_L = self.read_data_array(0x1a,1)[0]
            dis = diss_H << 8 | diss_L 
            return dis

        except Exception as e:
            warnings.warn(f"Read_Ultrasound_Sensor I2C error: {e}")
            return []

    def Read_IR_Sensor(self):
        """read infrared sensor data for line tracking sensor
        
        Returns:
            list: IR sensor data
        """
        try:
            reg = 0x0a
            track = self.read_data_array(reg, 1)
            x1 = (track >> 3) & 0x01
            x2 = (track >> 2) & 0x01
            x3 = (track >> 1) & 0x01
            x4 = track & 0x01
            return [x1,x2,x3,x4]

        except Exception as e:
            warnings.warn(f"Read_IR_Sensor I2C error: {e}")
            return []

    def Read_Key_Value(self):
        """read key value
        
        Returns:
            list: key pressed value
        """
        try:
            reg = 0x0d
            return self.read_data_array(reg, 1)

        except Exception as e:
            warnings.warn(f"Read_Key_Value I2C error: {e}")
            return []
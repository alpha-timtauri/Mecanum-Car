# The MIT License (MIT)
#
# Copyright (c) 2020 My Techno Talent, LLC For MicroPython
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`MPU6050`
====================================================

Driver class for the MPU6050 board.  Gyroscope, Accelerometer and Temperature
detection.

* Author(s): Kevin Thomas
"""
import machine

__version__ = "1.0.0"
__repo__ = "https://github.com/mytechnotalent/MicroPython_MPU6050.git"

MPU6050_ADDR                = 0x68
MPU6050_PWR_MGMT_1          = 0x6b
MPU6050_INT_ENABLE          = 0x38
MPU6050_TEMP_OUT_H          = 0x41
MPU6050_TEMP_OUT_L          = 0x42
MPU6050_ACCEL_XOUT_H        = 0x3B
MPU6050_ACCEL_XOUT_L        = 0x3C
MPU6050_ACCEL_YOUT_H        = 0x3D
MPU6050_ACCEL_YOUT_L        = 0x3E
MPU6050_ACCEL_ZOUT_H        = 0x3F
MPU6050_ACCEL_ZOUT_L        = 0x40
MPU6050_TEMP_OUT_H          = 0x41
MPU6050_TEMP_OUT_L          = 0x42
MPU6050_GYRO_XOUT_H         = 0x43
MPU6050_GYRO_XOUT_L         = 0x44
MPU6050_GYRO_YOUT_H         = 0x45
MPU6050_GYRO_YOUT_L         = 0x46
MPU6050_GYRO_ZOUT_H         = 0x47
MPU6050_GYRO_ZOUT_L         = 0x48
MPU6050_LSBC                = 340.0
MPU6050_TEMP_OFFSET         = 36.53
MPU6050_LSBG                = 16384.0
MPU6050_LSBDS               = 131.0


class MPU6050:
    """
    A class used to represent the MPU6050

    ...

    Attributes
    ----------
    i2c : <class 'SoftI2C'>
        Instance of the SoftI2C class
    addr : int
        Address of the i2c instance

    Methods
    -------
    combine_register_values(self, temp_h, temp_l)
        Combine reg values
    """
    def __init__(self, i2c, addr=MPU6050_ADDR):
        """
        Parameters
        ----------
        i2c : <class 'SoftI2C'>
            Instance of the SoftI2C class
        addr : int
            Address of the i2c instance
        """
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(MPU6050_ADDR, MPU6050_PWR_MGMT_1, bytes([0x00])) # SLEEP
        self.i2c.writeto_mem(MPU6050_ADDR, MPU6050_INT_ENABLE, bytes([0x01])) # DATA_RDY_EN

    def combine_register_values(self, temp_h, temp_l):
        """Combine register values which properly returns a combined 16-bit value

        Parameters
        ----------
        temp_h : int
            Temporary high-byte value
        temp_l : int
            Temporary low-byte value

        Returns
        -------
        int
            Returns an int of a combined 16-bit value
        """
        temp_h = temp_h[0]
        temp_l = temp_l[0]
        temp_h = temp_h << 8
        temp_data = temp_h | temp_l
        if temp_data & 0b1000000000000000:
            temp_data = -((temp_data ^ 0b1111111111111111) + 1)
        return temp_data

    def get_temp_data(self, i2c):
        """Get temperature data

        Parameters
        ----------
        i2c : <class 'SoftI2C'>
            Instance of the SoftI2C class

        Returns
        -------
        int
            Returns an int of temperature in farenheight
        """
        try:
            temp_h = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_TEMP_OUT_H, 1)
            temp_l = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_TEMP_OUT_L, 1)
            
            temp_c = (self.combine_register_values(temp_h, temp_l) / MPU6050_LSBC) + MPU6050_TEMP_OFFSET
            temp_f = (temp_c * 9/5) + 32
            temp_f = int('%2.f' % temp_f)
            return temp_c
        except OSError:
            pass
    
    def get_accel_data(self, i2c):
        """Get accelerometer data

        Parameters
        ----------
        i2c : <class 'SoftI2C'>
            Instance of the SoftI2C class

        Returns
        -------
        float
            Returns three floats, x y z in g's.
        """
        try:
            accel_x_h = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_XOUT_H, 1)
            accel_x_l = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_XOUT_L, 1)
            accel_y_h = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_YOUT_H, 1)
            accel_y_l = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_YOUT_L, 1)
            accel_z_h = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_ZOUT_H, 1)
            accel_z_l = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_ACCEL_ZOUT_L, 1)
            
            return [self.combine_register_values(accel_x_h, accel_x_l) / MPU6050_LSBG,
                    self.combine_register_values(accel_y_h, accel_y_l) / MPU6050_LSBG,
                    self.combine_register_values(accel_z_h, accel_z_l) / MPU6050_LSBG]
        except OSError:
                pass

    def get_gyro_data(self,i2c):
        """Get gyroscope data

        Parameters
        ----------
        i2c : <class 'SoftI2C'>
            Instance of the SoftI2C class

        Returns
        -------
        float
            Returns three floats, x y z in degrees per second
        """
        try:
            gyro_x_h = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_XOUT_H, 1)
            gyro_x_l = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_XOUT_L, 1)
            gyro_y_h = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_YOUT_H, 1)
            gyro_y_l = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_YOUT_L, 1)
            gyro_z_h = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_ZOUT_H, 1)
            gyro_z_l = self.i2c.readfrom_mem(MPU6050_ADDR, MPU6050_GYRO_ZOUT_L, 1)
            
            return [self.combine_register_values(gyro_x_h, gyro_x_l) / MPU6050_LSBDS,
                    self.combine_register_values(gyro_y_h, gyro_y_l) / MPU6050_LSBDS,
                    self.combine_register_values(gyro_z_h, gyro_z_l) / MPU6050_LSBDS]
        except OSError:
            pass

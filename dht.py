##########################################
# MLX90640 Thermal Camera w Raspberry Pi
# -- 2Hz Sampling with Simple Routine
##########################################
#
import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt


def getThermal():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=800000) # setup I2C
    mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate
    mlx_shape = (24,32)
    frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
    #t_array = []
    #t1 = time.monotonic()
    
    mlx.getFrame(frame) # read MLX temperatures into frame var
    data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
    #t_array.append(time.monotonic()-t1)
    return data_array

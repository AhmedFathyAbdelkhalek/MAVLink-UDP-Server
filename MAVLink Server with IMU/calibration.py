import mpu6050
import sys
import math
import time
from mpu6050 import ACCEL_XOUT_H, ACCEL_YOUT_H, ACCEL_ZOUT_H
from mpu6050 import GYRO_XOUT_H, GYRO_YOUT_H, GYRO_ZOUT_H

mpu = mpu6050
xacc,yacc,zacc,xgyro,ygyro,zgyro = 0,0,0,0,0,0 
flg = True
count = 0
t = 5

print("MPU6050 Calibration Software")
print("Please make sure that your MPU6050 is placed as horizontally as possible with the package letters facing upwards")

while t:
    secs = t
    timer = '{:2d}'.format(secs)
    print("Calibration starts in:" + timer, end="\r")
    time.sleep(1)
    t -= 1
print("\n")
    
try:
    mpu.MPU_Init()
    print("Calibrating MPU6050...")
except:
    print("MPU6050 not connceted. Aborting calibration...")
    sys.exit()

def data_split(x):  
    x1,x2,x3,y1,y2,y3 = tuple(float(i) for i in x.split(","))
    return x1,x2,x3,y1,y2,y3

while flg:
    for i in range(10000):
        try:
            dataList = data_split(mpu.mpuRead())
            xacc += dataList[0]
            yacc += dataList[1]
            zacc += dataList[2]
            xgyro += dataList[3]
            ygyro += dataList[4]
            zgyro +=  dataList[5]
            count +=1
            flg = False
        except:
            print("MPU6050 not connceted. Aborting calibration...")
            sys.exit()
        if count == 1000:
            print("...")
            count = 0
print("Your offsets are:")
print(xacc / i * 16384, yacc / i * 16384, (zacc / i * 16384) - 16384, xgyro / i * 131, ygyro / i * 131, zgyro / i * 131)
print("Offsets are printed as: xacc, yacc, zacc, xgyro, ygyro, zgyro")


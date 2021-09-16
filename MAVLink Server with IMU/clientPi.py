from pymavlink import mavutil
from msgdef import *
import socket
import mpu6050
from mpu6050 import ACCEL_XOUT_H, ACCEL_YOUT_H, ACCEL_ZOUT_H
from mpu6050 import GYRO_XOUT_H, GYRO_YOUT_H, GYRO_ZOUT_H

HOST = '127.0.0.1'  # The server's IP address
PORT = 65432  # The port used by the server
address   = (HOST, PORT) #Tuple to store address
bufferSize = 512

mpu = mpu6050 #Create an IMU object
mpu.MPU_Init() #Initialize IMU to read its data
print("Reading Data of Gyroscope and Accelerometer")

def data_split(x):  
    x1,x2,x3,y1,y2,y3 = tuple(float(i) for i in x.split(","))
    return x1,x2,x3,y1,y2,y3

def sendSensorData():
    global timer
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Create UDP socket
    s.settimeout(0.01) #Set a timeout so code can't get "stuck"
    sensorConnection = mavutil.mavlink_connection('udpout:localhost:14540') #Create MAVLink connection
    while True:
        s.sendto(b'a', address) #Send client port to server
        dataList = mpu.mpuRead() #Read IMU data
        xacc,yacc,zacc,xgyro,ygyro,zgyro = data_split(dataList) #Splitting IMU data into 6 variables
        sensorConnection.mav.highres_imu_send(0,xacc,yacc,zacc,xgyro,ygyro,zgyro,0,0,0,0,0,0,0,0) #Send IMU message through MAVLink

        try:
            actuatorSignal, addr = s.recvfrom(bufferSize) #Receive actuator signal
        except:
            continue
        print("Actuator Signal: {}".format(actuatorSignal.decode('utf-8')))

if __name__ == '__main__':
    sendSensorData()

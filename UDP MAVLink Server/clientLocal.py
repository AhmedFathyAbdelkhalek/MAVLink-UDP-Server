from pymavlink import mavutil
from msgdef import *
import socket

HOST = '127.0.0.1'  # The server's IP address
PORT = 65432  # The port used by the server
xacc, yacc, zacc, xgyro, ygyro, zgyro = 3,3,3,1,1,1 
address   = (HOST, PORT) #Tuple to store address
bufferSize = 512 

def client():    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Create UDP socket
    s.settimeout(0.001) #Set a timeout so code can't get "stuck"

    sensorConnection = mavutil.mavlink_connection('udpout:localhost:14540') #Create MAVLink connection
    while True:
        s.sendto(b'a', address) #Send client port to server
        sensorConnection.mav.highres_imu_send(0,xacc,yacc,zacc,xgyro,ygyro,zgyro,0,0,0,0,0,0,0,0) #Send IMU message through MAVLink

        try:
            actuatorSignal, addr= s.recvfrom(bufferSize) #Receive actuator signal
        except:
            continue
        print("Actuator Signal: {}".format(actuatorSignal.decode('utf-8')))

if __name__ == '__main__':
    client()
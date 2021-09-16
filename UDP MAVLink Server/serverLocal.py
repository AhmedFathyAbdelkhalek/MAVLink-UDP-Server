from flask import Flask, render_template
from pymavlink import mavutil
from msgdef import *
import socket
import os
import threading

HOST  = '127.0.0.1' #Server IP address
PORT   = 65432 #Server port
firstTime = True #Indicates whether its the first time to call my_server()
data_view = """""" #Store data to view on webpage
bufferSize = 512

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init')
def init():
    server()

@app.route('/data')
def data():
    return f"""<html><head><META HTTP-EQUIV="refresh"
           CONTENT="1"></head><body>"""+ data_view +'</body></html>'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def server():
    global data_view
    global firstTime

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Create a UDP socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Allow socket to reuse port
    s.bind((HOST, PORT)) #Bind socket to port

    sensorConnection = mavutil.mavlink_connection('udpin:localhost:14540') #Create a MAVLink connection to receive sensor data

    if firstTime:
        # Indicating the server has started
        print("Server Started waiting for clients to connect ")
        firstTime = False
    receiveDataAndSendActuatorSignal(sensorConnection, s) 

def receiveDataAndSendActuatorSignal(mavlink, socket):
    global data_view

    with socket:
        while True:
            try:
                data, addr = socket.recvfrom(bufferSize) #Receive UDP client port
            except:
                data = b''
            if len(data) != 0: #Checks if UDP client is connected
                imu_msg = mavlink.recv_match(type='HIGHRES_IMU', blocking=True, timeout = 0.001) #Receive sensor data through MAVLink
                if imu_msg == None:
                    continue #Restart loop if no data is received
                print(imu_msg)

                actuatorSignal = imu_msg.xacc * 1.5 #Generate some actuator signal
                encodedData = str(actuatorSignal).encode('utf-8')  # Encoding the signal
                socket.sendto(encodedData, addr)  # Send the byte stream to client

                data_view = f'''<p>Actuator Signal: {actuatorSignal}<br/> X Acceleration: {imu_msg.xacc}<br/> 
                Y Acceleration: {imu_msg.yacc}<br/> Z Acceleration: {imu_msg.zacc}<br/>
                X Gyro: {imu_msg.xgyro}<br/> Y Gyro: {imu_msg.ygyro}<br/> 
                Z Gyro: {imu_msg.zgyro}<br/></p>''' + data_view

def url():
    os.system('cmd /k "lt --port 5000"')

if __name__ == '__main__':
    threading.Thread(target=url).start() #Start local tunnel
    app.run(debug=True, host='0.0.0.0') #Build the Flask app
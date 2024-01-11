import serial
import json
import threading
import time
import sys
import write_db

kill_flag = False

PORT = str(input("COM Port (ex. COM10): "))
ser = serial.Serial()
ser.baudrate = 115200
ser.timeout = 0.1 
ser.port = PORT
ser.open()

class TelemetryLoop:
    global kill_flag
    def __init__(self):
        database = write_db.WriteDb()

        in_json = False
        json_str = ""

        while not kill_flag:
            line_byte = ser.readline()
            line_str = line_byte.strip().decode()
            if line_str == "{":
                in_json = True
            elif line_str == "}":
                in_json = False
                json_str += "}"
                try:
                    json_data = json.loads(json_str)
                    #print(json_data)
                except json.JSONDecodeError:
                    continue
                
                database.write(json_data)
                json_str = ""
            if in_json:
                json_str += line_str
                continue

class Commandloop:
    global kill_flag
    def __init__(self):
        while not kill_flag:
            cmd = input("Command: ")+'\n'
            ser.write(cmd.encode())

def close():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        kill_flag=True
        sys.exit

thread_Tlm = threading.Thread(target=TelemetryLoop, daemon=True)
thread_Com = threading.Thread(target=Commandloop, daemon=True)
thread_Tlm.start()
thread_Com.start()

close()
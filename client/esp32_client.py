import serial
import serial.tools.list_ports
import json
import threading
import time
import sys
import write_db
import csv_logger

kill_flag = False

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

PORT = str(input("COM Port (ex. COM10): "))
baudrate = str(input("Baudrate (option): "))
if baudrate == "":
    baudrate = 921600
ser = serial.Serial()
ser.baudrate = baudrate
ser.timeout = 0.1 
ser.port = PORT
ser.open()

logger = csv_logger.CsvLogger()

class TelemetryLoop:
    global kill_flag
    def __init__(self):
        database = write_db.WriteDb()

        in_json = False
        json_str = ""

        while not kill_flag:
            line_byte = ser.readline()
            line_str = ""
            try:
                line_str = line_byte.strip().decode()
            except:
                continue
            if line_str == "{":
                in_json = True
            elif line_str == "}":
                in_json = False
                json_str += "}"
                try:
                    json_data = json.loads(json_str)
                except json.JSONDecodeError:
                    print(json_str)
                    print("JSONDecodeError")
                    json_str = ""
                    continue
                json_str = ""
                try:
                    database.write_bulk(json_data)
                except:
                    print(json_data)
                    print("DBWriteError")
                    continue
                logger.write_data(json_data)
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
        logger.close()
        sys.exit

thread_Tlm = threading.Thread(target=TelemetryLoop, daemon=True)
thread_Com = threading.Thread(target=Commandloop, daemon=True)
thread_Tlm.start()
thread_Com.start()

close()
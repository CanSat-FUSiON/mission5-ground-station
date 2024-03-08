import json
import threading
import time
import sys
import write_db
import csv_logger
import socket
import struct
import contextlib


kill_flag = False

UDP_IP = "192.168.4.2"
UDP_PORT = 5000


sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

logger = csv_logger.CsvLogger()

class TelemetryLoop:
    global kill_flag
    def __init__(self):
        database = write_db.WriteDb()

        in_json = False
        json_str = ""

        while not kill_flag:
            sock.recv(4096)

            sf = sock.makefile()
            for line_byte in sf.readlines():
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
                    print(json_data)
                    logger.write_data(json_data)
                if in_json:
                    json_str += line_str
                    continue

class Commandloop:
    global kill_flag
    def __init__(self):
        while not kill_flag:
            cmd = input("Command: ")+'\n'


def close():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        kill_flag=True
        logger.close()
        sock.close()
        sys.exit

thread_Tlm = threading.Thread(target=TelemetryLoop, daemon=True)
thread_Com = threading.Thread(target=Commandloop, daemon=True)
thread_Tlm.start()
thread_Com.start()

close()
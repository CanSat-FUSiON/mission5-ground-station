import threading
import time
import random
import json
import sys
import numpy as np
import socket
import serial
import serial.tools.list_ports
import threading
import write_db
#import csv_logger

# デバッグモードの場合：true
Debug = False

# グローバル変数の設定
kill_flag = False
comport_data = []
commands = []

# comport選択処理
comport_is = str(input("COM Port (ex. COM10): "))
baudrate = str(input("Baudrate (option): "))
if baudrate == "":
    baudrate = 115200
ser = serial.Serial()
ser.baudrate = baudrate
ser.timeout = 0.01 
ser.port = comport_is
ser.open()

# ===============================================テレメトリloop内部処理===============================================

# processingにデータ送信
# ソケット設定
host = "127.0.0.1"
port_cmdUI = 10001
port_3dviewer = 10002
port_cmd_listener = 10003

class TelemetryLoop:
    global kill_flag
    def __init__(self):
        database = write_db.WriteDb()

        in_json = False
        json_str = ""

        while not kill_flag:
            line_byte = ser.readline()
            ser.reset_input_buffer()
            line_str = ""
            try:
                line_str = line_byte.strip().decode()
                try:
                    json_data = json.loads(line_str)
                    try:
                        database.write_bulk(json_data)
                        #print(line_str)
                        # 3D viewer
                        try:
                            #print("---------------------------------")
                            socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成
                            socket_client.connect((host, port_3dviewer))
                            data = line_str
                            socket_client.send(data.encode('utf-8')) #データを送信 Python3
                        except:
                            if Debug:
                                print("socket error")
                    except:
                        print(json_data)
                        print("DBWriteError")
                except json.JSONDecodeError:
                    #print(json_str)
                    if Debug :
                        print("!Error message!:JSONDecodeError\ncommand:")
                    
            except :
                print(".")

class Commandloop:
    def __init__(self):
        global kill_flag, commands
        threading.Thread(target=self.listen_for_commands, daemon=True).start()

        while not kill_flag:
            print("command:")
            cmd = input() + '\n'
            ser.write(cmd.encode())
            print("send!")
            if Debug:
                print("   " + cmd, end = "")
    
    def listen_for_commands(self):
        global commands
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port_cmd_listener))
            s.listen()
            while not kill_flag:
                conn, addr = s.accept()
                with conn:
                    while not kill_flag:
                        data = conn.recv(1024)
                        if not data:
                            break
                        cmd = data.decode('utf-8')
                        #commands.append(cmd)
                        #print(f"Received command from {addr}: {cmd}")
                        print("from_UI  :" + cmd)
                        ser.write(cmd.encode())
                        print("command:")

def close():
    global kill_flag
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        kill_flag = True
        sys.exit()

# ===============================================main処理===============================================
if __name__ == '__main__':
    # テレメトリループとコマンドループのスレッド開始
    thread_Tlm = threading.Thread(target=TelemetryLoop, daemon=True)
    thread_Com = threading.Thread(target=Commandloop, daemon=True)
    thread_Tlm.start()
    thread_Com.start()
    close()

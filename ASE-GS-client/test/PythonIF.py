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
import csv_logger

# デバッグモードの場合：true
Debug = False

# グローバル変数の設定
kill_flag = False
comport_data = []
commands = []

# ===============================================ランダムテレメトリ生成===============================================
# ランダムテレメトリの値の範囲
mode_range = (0, 3)
temperature_range = (-40.0, 85.0)
humidity_range = (0.0, 100.0)
pressure_range = (300.0, 1100.0)
roll_range = (-180.0, 180.0)
pitch_range = (-90.0, 90.0)
yaw_range = (-180.0, 180.0)
gyro_range = (-250.0, 250.0)
current_range = (0.0, 10.0)
voltage_range = (0.0, 5.0)

# ランダムテレメトリ生成
def generate_random_data():
    data = {
        "state_info": {
            "mode": random.randint(*mode_range)
        },
        "bme_data": {
            "temperature_deg_C": random.uniform(*temperature_range),
            "humidity_pct": random.uniform(*humidity_range),
            "pressure_hPa": random.uniform(*pressure_range)
        },
        "euler_angle_deg": {
            "roll": random.uniform(*roll_range),
            "pitch": random.uniform(*pitch_range),
            "yaw": random.uniform(*yaw_range)
        },
        "gyro_deg_sec": {
            "x": random.uniform(*gyro_range),
            "y": random.uniform(*gyro_range),
            "z": random.uniform(*gyro_range)
        },
        "Battery_current_A": {
            "A": random.uniform(*current_range)
        },
        "ADC_current_A": {
            "_1": random.uniform(*current_range),
            "_2": random.uniform(*current_range),
            "_3": random.uniform(*current_range),
            "_4": random.uniform(*current_range)
        },
        "thermistor_current": {
            "_1": random.uniform(*current_range),
            "_2": random.uniform(*current_range)
        }
    }
    return json.dumps(data)

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
            time.sleep(0.5)
            json_str = generate_random_data()
            json_data = json.loads(json_str)

            try:
                database.write_bulk(json_data)  # データベースへの書き込みは省略
                print(json_str)
            except:
                print("DBWriteError")
                sys.exit()
            # 3D viewer
            try:
                socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成
                socket_client.connect((host, port_3dviewer))
                data = json_str
                socket_client.send(data.encode('utf-8')) #データを送信 Python3
            except:
                if Debug:
                    print("socket error")

class Commandloop:
    def __init__(self):
        global kill_flag, commands
        threading.Thread(target=self.listen_for_commands, daemon=True).start()

        while not kill_flag:
            print("command:")
            cmd = input() + '\n'
            #commands.append(cmd)
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

import serial
import serial.tools.list_ports
import json
import threading
import time
import sys
import write_db
import csv_logger
import json
import random

kill_flag = False

"""
# ComPortリスト取得
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

# ComPort設定
PORT = str(input("COM Port (ex. COM10): ")) # Port番号設定
baudrate = str(input("Baudrate (option): ")) # ボーレート設定
if baudrate == "": # ボーレート未設定の場合921600
    baudrate = 921600
ser = serial.Serial()
ser.baudrate = baudrate
ser.timeout = 0.1 
ser.port = PORT
ser.open()

# 今回はlog無効
# logger = csv_logger.CsvLogger()
"""

# ランダムテレメトリ生成関数
# 各パラメータの取りうる範囲
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

# ランダムに数値を生成する関数
def generate_random_data():
    data = {
        "state_info": {
            "mode": random.randint(*mode_range)
        },
        "temperature_humidity_pressure": {
            "temperature_deg_C": random.uniform(*temperature_range),
            "humidity_pct": random.uniform(*humidity_range),
            "pressure_hPa": random.uniform(*pressure_range)
        },
        "orientation_euler": {
            "roll": random.uniform(*roll_range),
            "pitch": random.uniform(*pitch_range),
            "yaw": random.uniform(*yaw_range)
        },
        "gyro": {
            "gyro_x": random.uniform(*gyro_range),
            "gyro_y": random.uniform(*gyro_range),
            "gyro_z": random.uniform(*gyro_range)
        },
        "power_current_voltage": {
            "A": random.uniform(*current_range),
            "V": random.uniform(*voltage_range)
        }
    }
    return data

class TelemetryLoop:
    global kill_flag
    def __init__(self):
        database = write_db.WriteDb()

        in_json = False
        json_str = ""

        while not kill_flag:
            json_str = generate_random_data()

            try:
                json_data = json.loads(json_str)
                database.write_bulk(json_data)
            except:
                print("DBWriteError")
                continue

class Commandloop:
    global kill_flag
    def __init__(self):
        while not kill_flag:
            cmd = input("Command: ")+'\n'
            #ser.write(cmd.encode())
            print(cmd) # ダミーなので

def close():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        kill_flag=True
        # logger.close()
        sys.exit

thread_Tlm = threading.Thread(target=TelemetryLoop, daemon=True)
thread_Com = threading.Thread(target=Commandloop, daemon=True)
thread_Tlm.start()
thread_Com.start()

close()
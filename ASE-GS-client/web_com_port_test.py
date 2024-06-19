from flask import Flask, render_template_string, jsonify
import threading
import time
import random
import json
import sys
import numpy as np
import socket
import threading

# グローバル変数の設定
kill_flag = False
comport_data = []

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
        "temperature_humidity_pressure": {
            "temperature_deg_C": random.uniform(*temperature_range),
            "humidity_pct": random.uniform(*humidity_range),
            "pressure_hPa": random.uniform(*pressure_range)
        },
        "euler_angle": {
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
    return json.dumps(data)

# processingにデータ送信
# ソケット設定
host = "127.0.0.1"
port = 10001
socket_client = None

def socket_thread():
    global socket_client
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((host, port))

def send_data(data):
    global socket_client
    if socket_client is not None:
        # data = f"{roll},{pitch},{yaw}"
        socket_client.send(data.encode('utf-8'))

# テレメトリからオイラー角だけ取り出す
# roll, pitch, yaw のパラメータをカンマ区切りの文字列として取り出す関数
def extract_euler_angle(data):
    orientation = data.get("euler_angle", {})
    roll = orientation.get("roll", None)
    pitch = orientation.get("pitch", None)
    yaw = orientation.get("yaw", None)
    # カンマ区切りの文字列として結合
    orientation_str = f"{roll}, {pitch}, {yaw}"
    return orientation_str

class TelemetryLoop:
    def __init__(self):
        global kill_flag
        in_json = False
        json_str = ""

        while not kill_flag:
            json_str = generate_random_data()
            json_data = json.loads(json_str)
            # InfluxDB & txt_tlm
            try:
                # database.write_bulk(json_data)  # データベースへの書き込みは省略
                comport_data.insert(0, json_str)
                if len(comport_data) > 10:
                    comport_data.pop()
                time.sleep(1)
            except:
                print("DBWriteError")
                sys.exit()

            # 3D viewer
            try:
                host = "127.0.0.1" #Processingで立ち上げたサーバのIPアドレス
                port = 10001       #Processingで設定したポート番号
                socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成
                socket_client.connect((host, port))
                data = extract_euler_angle(json_data)
                # print(json_data)
                socket_client.send(data.encode('utf-8')) #データを送信 Python3
            except:
                print("socket error")

class Commandloop:
    def __init__(self):
        global kill_flag
        while not kill_flag:
            cmd = input("Command: ")+'\n'
            # ser.write(cmd.encode())  # シリアルポートへの書き込みは省略
            print(cmd)

def close():
    global kill_flag
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        kill_flag = True
        sys.exit()

# Flaskの設定
app = Flask(__name__)

# Template for the web page
template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Comport Data</title>
    <style>
      body {
        background-color: black;
        color: white;
        font-family: monospace;
      }
      ul {
        list-style-type: none;
        padding: 0;
      }
      li {
        white-space: pre-wrap;
      }
    </style>
    <script type="text/javascript">
      function fetchData() {
        fetch('/data')
          .then(response => response.json())
          .then(data => {
            let dataList = document.getElementById('dataList');
            dataList.innerHTML = '';
            data.forEach(item => {
              let li = document.createElement('li');
              li.textContent = JSON.stringify(item, null, 2);
              dataList.appendChild(li);
            });
          });
      }
      setInterval(fetchData, 1000); // Update data every second
    </script>
  </head>
  <body onload="fetchData()">
    <h1>Comport Data</h1>
    <ul id="dataList">
    </ul>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(template)

@app.route('/data')
def data():
    return jsonify(comport_data)

def start_flask():
    app.run(debug=False, use_reloader=False, port=8080)

if __name__ == '__main__':
    # Flaskスレッドの開始
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # テレメトリループとコマンドループのスレッド開始
    thread_Tlm = threading.Thread(target=TelemetryLoop, daemon=True)
    thread_Com = threading.Thread(target=Commandloop, daemon=True)
    thread_Tlm.start()
    thread_Com.start()

    close()

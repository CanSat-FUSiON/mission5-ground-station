import os
import json
import random
import time
import sys
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class WriteDb:
    def __init__(self):
        # Influx接続用データ値
        self.token = "my-super-secret-auth-token"
        self.org = "FUSiON"
        self.bucket = "Data"
        self.url = "http://localhost:8086"

        # Client作成
        self.client = influxdb_client.InfluxDBClient(url=self.url, token=self.token, org=self.org)

        # API作成
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        #self.write_api = self.client.write_api()

    def write(self, json_data):
        #全体で0.6sかかってる.
        #start_time = time.time()
        for tagkey,apps in json_data.items():
            # API用のPOINT作成
            #0.05sくらい
            #start_time = time.time()
            point = Point("FUSiON_CanSat")
            # POINTにタグ追加
            point.tag("_tag",tagkey)
            # Debug
            # print("============= _Tag = {} =============".format(tagkey))
            # FIELD分だけ回す愚直解法
            #0.05sくらいかかってる．
            #start_time = time.time()
            for fieldkey,values in apps.items():
                #POINTにFIELDを追加
                point.field(tagkey+'_'+fieldkey, values)
            # Debug    
            # print("Line:{}".format(point))
            # DB書き込み
            #0.05sくらいかかってる．
            #start_time = time.time()
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
            #end_time = time.time()
            #time_diff = end_time - start_time
            #print(time_diff)

def create_rand():
        randint_value = [random.randint(0,1) for i in range(10)]
        randint_value2 = [random.randint(0,100) for i in range(5)]
        #print(randint_value)
        rand0to1_value = [random.random() for i in range(6)]
        #print(rand0to1_value)
        randfloat_value = [random.uniform(-100,100) for i in range(22)]
        #print(randfloat_value)
        randfloat_value2 = [random.uniform(0,10) for i in range(4)]
        #print(randfloat_value)

        json_object = {
            "fusion_core_mode":{
                "mode":randint_value[0]
            },
            "app_bme280":{
                "valid":randint_value[1],
                "temperature_degC":randfloat_value[0],
                "humidity_pct":randfloat_value[1],
                "pressure_hPa":randfloat_value[2],
                "altitude_m":randfloat_value[3]
            },
            "app_bno055":{
                "valid":randint_value[2],
                "accel_x_mss":randfloat_value[4],
                "accel_y_mss":randfloat_value[5],
                "accel_z_mss":randfloat_value[6],
                "mag_x_uT":randfloat_value[7],
                "mag_y_uT":randfloat_value[8],
                "mag_z_uT":randfloat_value[9],
                "gyro_x_degs":randfloat_value[10],
                "gyro_y_degs":randfloat_value[11],
                "gyro_z_degs":randfloat_value[12],
                "orient_x_deg":randfloat_value[13],
                "orient_y_deg":randfloat_value[14],
                "orient_z_deg":randfloat_value[15],
                "quaternion_w":randfloat_value[16],
                "quaternion_x":randfloat_value[17],
                "quaternion_y":randfloat_value[18],
                "quaternion_z":randfloat_value[19],
                "mag_direction_deg":randfloat_value[20],
                "count":randint_value2[0]
            },
            "app_current_L":{
                "valid":randint_value[3],
                "current_mA":randfloat_value2[0],
                "voltage_V":randfloat_value2[1]
            },
            "app_current_R":{
                "valid":randint_value[4],
                "current_mA":randfloat_value2[2],
                "voltage_V":randfloat_value2[3]
            },
            "app_flight_pin":{
                "valid":randint_value[5],
                "connect":randint_value[6],
                "disconnect_count":randint_value2[1]
            },
            "app_gnss":{
                "satellites":randint_value2[2],
                "hdop":2.95,
                "location_valid":randint_value[7],
                "latitude_deg":35.771491,
                "longitude_deg":139.863740,
                "time_ms":239575000,
                "altitude_m":124.20,
                "course_deg":0.00,
                "speed_ms":0.02
            },
            "app_motor_L":{
                "throttle":rand0to1_value[0],
                "pwm_1_duty":rand0to1_value[1],
                "pwm_2_duty":rand0to1_value[2]
            },
            "app_motor_R":{
                "throttle":rand0to1_value[3],
                "pwm_1_duty":rand0to1_value[4],
                "pwm_2_duty":rand0to1_value[5]
            },
            "app_spresense":{
                "goal_detected":randint_value[8]
            },
            "app_simulator":{
                "mode":randint_value[9]
            },
            "app_release_detection":{
                "previous_altitude_m":randfloat_value[21],
                "descent_count":randint_value2[3],
                "descent_count_threshold":randint_value2[4],
                "altitude_m_threshold":1.50
            }
        }
        # objectをjsonフォーマットの文字列に変換
        json_str = json.dumps(json_object)
        #print(json_str)
        return json_str

cnt = 0

while True:
    print("sending...{}".format(cnt))
    json_str = create_rand()
    try:
        json_data = json.loads(json_str)
        #start_time = time.time()
        WriteDb().write(json_data)
        #end_time = time.time()
        cnt += 1
    except KeyboardInterrupt:
        sys.exit
    except:
        print(json_data)
        print("DBWriteError")
        continue
    #time_diff = end_time - start_time
    #print(time_diff)
    if cnt == 100:
        print("設定された実行数です")
        sys.exit()
    #time.sleep(0.05)
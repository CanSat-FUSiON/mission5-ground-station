import json
import sys
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#Json判定用（間違ってたらエラー吐くだけの子なのでいらないかも）
def is_json(json_str):
    '''
    json_strがjson.loads可能か判定
    '''
    result = False
    try:
        json.loads(json_str)
        result = True
    except json.JSONDecodeError as jde:
        print( "[", json_str, "] is not in json format. \n", sys.exc_info())

    return result

#Influx接続用データ値
token = "my-super-secret-auth-token"
org = "FUSiON"
bucket = "Data"
url = "http://localhost:8086"

#Client作成
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

#API作成
write_api = client.write_api(write_options=SYNCHRONOUS)

#TEST用
ok_object = {
   "fusion_core_mode":{
      "mode":0
   },
   "app_bme280":{
      "valid":1,
      "temperature_degC":20.43,
      "humidity_pct":79.93,
      "pressure_hPa":1021.15,
      "altitude_m":-65.60
   },
   "app_bno055":{
      "valid":1,
      "accel_x_mss":-0.37,
      "accel_y_mss":0.62,
      "accel_z_mss":9.50,
      "mag_x_uT":-0.69,
      "mag_y_uT":24.06,
      "mag_z_uT":-36.69,
      "gyro_x_degs":0.00,
      "gyro_y_degs":0.00,
      "gyro_z_degs":0.00,
      "orient_x_deg":3.94,
      "orient_y_deg":2.19,
      "orient_z_deg":0.08,
      "quaternion_w":0.999207,
      "quaternion_x":0.034363,
      "quaternion_y":0.019165,
      "quaternion_z":0.000000,
      "mag_direction_deg":1.64,
      "count":0
   },
   "app_current_L":{
      "valid":1,
      "current_mA":0.00,
      "voltage_V":11.42
   },
   "app_current_R":{
      "valid":1,
      "current_mA":1.00,
      "voltage_V":11.43
   },
   "app_flight_pin":{
      "valid":0,
      "connect":1,
      "disconnect_count":0
   },
   "app_gnss":{
      "satellites":4,
      "hdop":2.95,
      "location_valid":1,
      "latitude_deg":35.771491,
      "longitude_deg":139.863740,
      "time_ms":239575000,
      "altitude_m":124.20,
      "course_deg":0.00,
      "speed_ms":0.02
   },
   "app_motor_L":{
      "throttle":0.00,
      "pwm_1_duty":0.00,
      "pwm_2_duty":-0.00
   },
   "app_motor_R":{
      "throttle":0.00,
      "pwm_1_duty":0.00,
      "pwm_2_duty":-0.00
   },
   "app_spresense":{
      "goal_detected":0
   },
   "app_simulator":{
      "mode":0
   },
   "app_release_detection":{
      "previous_altitude_m":-65.60,
      "descent_count":0,
      "descent_count_threshold":3,
      "altitude_m_threshold":1.50
   }
}
# objectをjsonフォーマットの文字列に変換
ok_json_str = json.dumps(ok_object)
#Debug
print(ok_json_str)

#ループ
#while(1):
#JSON判定
if(is_json(ok_json_str)):
    #JSON文字列の読み込み
    json_object = json.loads(ok_json_str)
    #Tag分だけ回す愚直解法
    for tagkey in json_object:
        # API用のPOINT作成
        point = Point("FUSiON_CanSat")
        #POINTにタグ追加
        point.tag("_tag",tagkey)
        #Debug
        print("============= _Tag = {} =============".format(tagkey))
        #FIELD分だけ回す愚直解法
        for fieldkey,values in json_object[tagkey].items():
            #POINTにFIELDを追加
            point.field(fieldkey, values)
        #Debug    
        print("Line:{}".format(point))
        #DB書き込み
        write_api.write(bucket=bucket, org=org, record=point)
#Debug
print("--- End ---")
#  time.sleep(10) # separate points by 10 second
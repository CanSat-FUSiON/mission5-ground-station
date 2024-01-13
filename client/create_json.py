import os
import json
import random

class Create_Json:
    def __init__(self):
        randint_value = [random.randint(0,1) for i in range(10)]
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
                "count":0
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
                "disconnect_count":0
            },
            "app_gnss":{
                "satellites":4,
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
                "descent_count":0,
                "descent_count_threshold":3,
                "altitude_m_threshold":1.50
            }
        }
        # objectをjsonフォーマットの文字列に変換
        json_str = json.dumps(json_object)
        #print(json_str)

        with open('./dummy_rand.json','w') as f:
            f.write(json_str)
            f.close()
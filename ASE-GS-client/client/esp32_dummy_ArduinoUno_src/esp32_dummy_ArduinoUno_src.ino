#include <Arduino.h>

int mode = 0;

float randomFloat(float min, float max) {
  return min + static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / (max - min)));
}

void setup() {
  Serial.begin(115200);  // シリアル通信の初期化
  randomSeed(analogRead(0));  // ランダムシードを設定
}

void loop() {
  // ランダムなテレメトリデータを生成
  // ! 適当な文字列を受信したら適当にモードの部分だけ変更する
  if(Serial.available() > 0){
    char c = Serial.read();
    if(c != '\r' && c != '\n' && c != '\r\n'){
        mode = c - '0';
    }
  }
  //int mode = random(0, 4);
  float temperature = randomFloat(-40.0, 85.0);
  float humidity = randomFloat(0.0, 100.0);
  float pressure = randomFloat(300.0, 1100.0);
  float roll = randomFloat(-180.0, 180.0);
  float pitch = randomFloat(-90.0, 90.0);
  float yaw = randomFloat(-180.0, 180.0);
  float gyroX = randomFloat(-250.0, 250.0);
  float gyroY = randomFloat(-250.0, 250.0);
  float gyroZ = randomFloat(-250.0, 250.0);
  float batteryCurrent = randomFloat(0.0, 10.0);
  float adcCurrent1 = randomFloat(0.0, 10.0);
  float adcCurrent2 = randomFloat(0.0, 10.0);
  float adcCurrent3 = randomFloat(0.0, 10.0);
  float adcCurrent4 = randomFloat(0.0, 10.0);
  float thermistorCurrent1 = randomFloat(0.0, 10.0);
  float thermistorCurrent2 = randomFloat(0.0, 10.0);

  // JSONデータを構築
  // !ここの書き方がめちゃくちゃ重要
  // 説明】:最初に{+改行, 最後に}+改行, 内容としては項目ごとに改行というような書き方をする必要がある
  //*
  String json = "{\n";
  json += "\t\"state_info\":{\"mode\":" + String(mode) + "},\n";
  json += "\t\"bme_data\":{\"temperature_deg_C\":" + String(temperature, 2) + ", \"humidity_pct\":" + String(humidity, 2) + ", \"pressure_hPa\":" + String(pressure, 2) + "},\n";
  json += "\t\"euler_angle_deg\":{\"roll\":" + String(roll, 2) + ", \"pitch\":" + String(pitch, 2) + ", \"yaw\":" + String(yaw, 2) + "},\n";
  json += "\t\"gyro_deg_sec\":{\"x\":" + String(gyroX, 2) + ", \"y\":" + String(gyroY, 2) + ", \"z\":" + String(gyroZ, 2) + "},\n";
  json += "\t\"Battery_current_A\":{\"A\":" + String(batteryCurrent, 2) + "},\n";
  json += "\t\"ADC_current_A\":{\"_1\":" + String(adcCurrent1, 2) + ", \"_2\":" + String(adcCurrent2, 2) + ", \"_3\":" + String(adcCurrent3, 2) + ", \"_4\":" + String(adcCurrent4, 2) + "},\n";
  json += "\t\"thermistor_current\":{\"_1\":" + String(thermistorCurrent1, 2) + ", \"_2\":" + String(thermistorCurrent2, 2) + "}\n";
  json += "}\n";

  Serial.print(json);  // シリアルポートにJSON文字列を送信*/

  /*/ JSON形式でシリアル出力
  Serial.print("{\"state_info\":{\"mode\":");
  Serial.print(mode);
  Serial.print("},\"bme_data\":{\"temperature_deg_C\":");
  Serial.print(temperature);
  Serial.print(",\"humidity_pct\":");
  Serial.print(humidity);
  Serial.print(",\"pressure_hPa\":");
  Serial.print(pressure);
  Serial.print("},\"euler_angle_deg\":{\"roll\":");
  Serial.print(roll);
  Serial.print(",\"pitch\":");
  Serial.print(pitch);
  Serial.print(",\"yaw\":");
  Serial.print(yaw);
  Serial.print("},\"gyro_deg_sec\":{\"x\":");
  Serial.print(gyroX);
  Serial.print(",\"y\":");
  Serial.print(gyroY);
  Serial.print(",\"z\":");
  Serial.print(gyroZ);
  Serial.print("},\"Battery_current_A\":{\"A\":");
  Serial.print(batteryCurrent);
  Serial.print("},\"ADC_current_A\":{\"_1\":");
  Serial.print(adcCurrent1);
  Serial.print(",\"_2\":");
  Serial.print(adcCurrent2);
  Serial.print(",\"_3\":");
  Serial.print(adcCurrent3);
  Serial.print(",\"_4\":");
  Serial.print(adcCurrent4);
  Serial.print("},\"thermistor_current\":{\"_1\":");
  Serial.print(thermistorCurrent1);
  Serial.print(",\"_2\":");
  Serial.print(thermistorCurrent2);
  Serial.println("}}");//*/


  delay(1000);  // 1秒待機
}

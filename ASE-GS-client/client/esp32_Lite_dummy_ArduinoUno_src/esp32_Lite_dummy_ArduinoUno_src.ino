#include <MsTimer2.h>

int mode = 0;

// タイマー割り込みの間隔（ミリ秒）
const unsigned long interval = 1000;

// タイマ割り込み判定フラグ
bool timer_flag = false;

// 割り込みハンドラ
void timerISR() {
  // LEDの状態を反転
  timer_flag = true;
}

float randomFloat(float min, float max) {
  return min + static_cast<float>(rand()) / (static_cast<float>(RAND_MAX / (max - min)));
}

// タイマ定期実行関数
void send_json() {
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

  // JSON形式でシリアル出力
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
  Serial.println("}}");
  timer_flag = false;
}

void setup() {
  Serial.begin(115200);  // シリアル通信の初期化
  randomSeed(analogRead(0));  // ランダムシードを設定

  // タイマー割り込みを設定
  MsTimer2::set(interval, timerISR);

  // タイマー割り込みを開始
  MsTimer2::start();
}

void loop() {
  // ! 適当な文字列を受信したら適当にモードの部分だけ変更する
  if(Serial.available() > 0){
    char c = Serial.read();
    if(c != '\r' && c != '\n' && c != '\r\n'){
        mode = c - '0';
    }
  }
  if(timer_flag){
    send_json();
  }
}

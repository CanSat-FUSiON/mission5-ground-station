
import processing.net.*;

int port = 10002; // 適当なポート番号を設定

Server server;

float roll=0, pitch=0, yaw=0;

// Euler angle
PVector x_unit = new PVector(1,0,0);
PVector y_unit = new PVector(0,1,0);
PVector z_unit = new PVector(0,0,-1);

void setup() {
    size(800,800,P3D);
    server = new Server(this, port);
    println("server address: " + server.ip()); // IPアドレスを出力
}

void draw() {
    // 画面初期化
    background(200);
    // 受信とパケットパース(仮)
    rx_pars();
    // 座標変換と表示
    pushMatrix();
        translate(400, 400);
        rotateX(radians(-90));
        rotateZ(radians(-90));
        rotateY(radians(-30));
        rotateZ(radians(-20));
        satellite_draw();
    popMatrix();
}

void rx_pars(){
    Client client = server.available();
    if (client !=null) {
        String whatClientSaid = client.readString();
        if (whatClientSaid != null) {
            // jsonオブジェクトを生成
            JSONObject json = parseJSONObject(whatClientSaid);
            // euler_angleオブジェクトを取得
            JSONObject eulerAngle = json.getJSONObject("euler_angle");
            // roll,pitch,yawをfloat型に変換
            // roll, pitch, yawの値を取得してfloat型に変換
            roll = eulerAngle.getFloat("roll");
            pitch = eulerAngle.getFloat("pitch");
            yaw = eulerAngle.getFloat("yaw");

        } 
    } 
}

// draw satellite 3D CG
void satellite_draw(){
    // Reference coordinate system process
    float k = 150;
    arrow(0,0,0,k*x_unit.x,k*x_unit.y,k*x_unit.z,k,0,0);
    arrow(0,0,0,k*y_unit.x,k*y_unit.y,k*y_unit.z,0,k,0);
    arrow(0,0,0,k*z_unit.x,k*z_unit.y,k*z_unit.z,0,0,k);
    // Euler Angle rotation process
    rotateZ(radians((float)yaw));// 3 yaw
    rotateY(radians(-(float)pitch));// 2 pitch
    rotateX(radians(-(float)roll));// 1 roll
    // Body coordinate system process
    k = 200;
    arrow(0,0,0,k*x_unit.x,k*x_unit.y,k*x_unit.z,k,0,0);
    arrow(0,0,0,k*y_unit.x,k*y_unit.y,k*y_unit.z,0,k,0);
    arrow(0,0,0,k*z_unit.x,k*z_unit.y,k*z_unit.z,0,0,k);
    fill(255,255,0);
    stroke(0);
    strokeWeight(3);
    k = 40;
    box(2*k,3*k,1*k);
}
//*/
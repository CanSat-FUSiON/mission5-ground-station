import processing.net.*;

int port = 10001; // 適当なポート番号を設定

Server server;

void setup() {
    server = new Server(this, port);
    println("server address: " + server.ip()); // IPアドレスを出力
}

void draw() {
    Client client = server.available();
    if (client !=null) {
        String whatClientSaid = client.readString();
        if (whatClientSaid != null) {
            //println(whatClientSaid); // Pythonからのメッセージを出力
            // jsonオブジェクトを生成
            JSONObject json = parseJSONObject(whatClientSaid);
            // euler_angleオブジェクトを取得
            JSONObject eulerAngle = json.getJSONObject("euler_angle");
            // roll,pitch,yawをfloat型に変換
            // roll, pitch, yawの値を取得してfloat型に変換
            float roll = eulerAngle.getFloat("roll");
            float pitch = eulerAngle.getFloat("pitch");
            float yaw = eulerAngle.getFloat("yaw");

            // 結果を出力
            println("Roll: " + roll);
            println("Pitch: " + pitch);
            println("Yaw: " + yaw);
        } 
    } 
}

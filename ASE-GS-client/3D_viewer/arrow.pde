
// 以下のサイトのコードを利用
// 理系大学院生の知識の森：『Processingで矢印を描く方法（３次元）』
//   (https://okasho-engineer.com/processing-3d-arrow/)
void cone(float L, float radius, float Color1, float Color2, float Color3) {
    translate(0, 0, 10);  // コーンのオフセット
    float x, y;
    noStroke();
    fill(Color1, Color2, Color3);
    beginShape(TRIANGLE_FAN);  // 底面の円の作成
    vertex(0, 0, -L);
    for(float i=0; i<2*PI; i+=0.01) {
        x = radius*cos(i);
        y = radius*sin(i);
        vertex(x, y, -L);
    }

    endShape(CLOSE);
    beginShape(TRIANGLE_FAN);  // 側面の作成
    vertex(0, 0, 0);
    for(float i=0; i<2*PI; i+=0.01) {
        x = radius*cos(i);
        y = radius*sin(i);
        vertex(x, y, -L);
    }
    endShape(CLOSE);
}

// 以下のサイトのコードを利用
// 理系大学院生の知識の森：『Processingで矢印を描く方法（３次元）』
//   (https://okasho-engineer.com/processing-3d-arrow/)
void arrow(float x1, float y1, float z1, float x2, float y2, float z2, float Color1, float Color2, float Color3) {
    float arrowLength = 10;
    float arrowAngle = 0.5;
    float phi = -atan2(y2-y1, x2-x1);
    float theta = 0.5*PI - atan2(z2-z1, x2-x1);
    stroke(Color1, Color2, Color3);
    strokeWeight(4); 
    line(x1, y1, z1, x2, y2, z2);
    strokeWeight(1); 
    pushMatrix();
    translate(x2, y2, z2);
    rotateY(theta);
    rotateX(phi);
    cone(arrowLength, arrowLength*sin(arrowAngle), Color1, Color2, Color3);
    popMatrix();
}
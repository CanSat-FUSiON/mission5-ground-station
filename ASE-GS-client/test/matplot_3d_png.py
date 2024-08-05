import socket
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# サーバーのポート番号
PORT = 10002

# サーバーのセットアップ
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', PORT))
server_socket.listen(1)
print(f"Server started on port {PORT}")

# 初期のオイラー角
roll = pitch = yaw = 0

# 座標変換用のユニットベクトル
x_unit = np.array([1, 0, 0])
y_unit = np.array([0, 1, 0])
z_unit = np.array([0, 0, -1])

def read_from_client():
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    data = client_socket.recv(1024).decode('utf-8')
    client_socket.close()
    if data:
        # JSONオブジェクトをパース
        json_data = json.loads(data)
        euler_angle = json_data.get("euler_angle_deg", {})
        global roll, pitch, yaw
        roll = euler_angle.get("roll", 0)
        pitch = euler_angle.get("pitch", 0)
        yaw = euler_angle.get("yaw", 0)

def rotation_matrix_x(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])

def rotation_matrix_y(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ])

def rotation_matrix_z(angle):
    c, s = np.cos(np.radians(angle)), np.sin(np.radians(angle))
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])

def draw_satellite(ax):
    ax.clear()
    k = 150
    
    # 参照座標系の矢印
    ax.quiver(0, 0, 0, k*x_unit[0], k*x_unit[1], -k*x_unit[2], color='r')
    ax.quiver(0, 0, 0, k*y_unit[0], k*y_unit[1], -k*y_unit[2], color='g')
    ax.quiver(0, 0, 0, k*z_unit[0], k*z_unit[1], -k*z_unit[2], color='b')
    
    # オイラー角での回転
    R = np.dot(
        np.dot(
            rotation_matrix_z(yaw),
            rotation_matrix_y(-pitch)
        ),
        rotation_matrix_x(-roll)
    )
    
    # 本体座標系の矢印
    rotated_x_unit = R.dot(x_unit) * 200
    rotated_y_unit = R.dot(y_unit) * 200
    rotated_z_unit = R.dot(z_unit) * 200
    
    ax.quiver(0, 0, 0, rotated_x_unit[0], rotated_x_unit[1], -rotated_x_unit[2], color='r')
    ax.quiver(0, 0, 0, rotated_y_unit[0], rotated_y_unit[1], -rotated_y_unit[2], color='g')
    ax.quiver(0, 0, 0, rotated_z_unit[0], rotated_z_unit[1], -rotated_z_unit[2], color='b')
    
    # ボックスの描画
    k = 40
    box_vertices = np.array([
        [-k, -k, -k],
        [ k, -k, -k],
        [ k,  k, -k],
        [-k,  k, -k],
        [-k, -k,  k],
        [ k, -k,  k],
        [ k,  k,  k],
        [-k,  k,  k]
    ])
    
    box_faces = [
        [box_vertices[0], box_vertices[1], box_vertices[2], box_vertices[3]],
        [box_vertices[4], box_vertices[5], box_vertices[6], box_vertices[7]],
        [box_vertices[0], box_vertices[1], box_vertices[5], box_vertices[4]],
        [box_vertices[2], box_vertices[3], box_vertices[7], box_vertices[6]],
        [box_vertices[0], box_vertices[3], box_vertices[7], box_vertices[4]],
        [box_vertices[1], box_vertices[2], box_vertices[6], box_vertices[5]]
    ]
    
    transformed_vertices = (R.dot(box_vertices.T) + np.array([[0], [0], [0]])).T
    
    box_faces_transformed = [
        [transformed_vertices[0], transformed_vertices[1], transformed_vertices[2], transformed_vertices[3]],
        [transformed_vertices[4], transformed_vertices[5], transformed_vertices[6], transformed_vertices[7]],
        [transformed_vertices[0], transformed_vertices[1], transformed_vertices[5], transformed_vertices[4]],
        [transformed_vertices[2], transformed_vertices[3], transformed_vertices[7], transformed_vertices[6]],
        [transformed_vertices[0], transformed_vertices[3], transformed_vertices[7], transformed_vertices[4]],
        [transformed_vertices[1], transformed_vertices[2], transformed_vertices[6], transformed_vertices[5]]
    ]
    
    poly3d = Poly3DCollection(box_faces_transformed, facecolors='yellow', edgecolors='black', linewidths=1, alpha=0.5)
    ax.add_collection3d(poly3d)
    
    # 軸の設定
    ax.set_xlim(-250, 250)
    ax.set_ylim(-250, 250)
    ax.set_zlim(-250, 250)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

# メインの描画ループ
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def update_plot():
    read_from_client()
    draw_satellite(ax)
    plt.draw()
    plt.pause(1)

# イベントループ
while plt.fignum_exists(fig.number):
    update_plot()

plt.close(fig)
server_socket.close()

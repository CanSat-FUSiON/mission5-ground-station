import socket
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh
import os

# スクリプトのディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)

# 相対パスを絶対パスに変換
relative_path = 'CubeSat-edu2-convert.stl'
full_path = os.path.join(script_dir, relative_path)

# 絶対パスを出力（デバッグ用）
print(f"Absolute path: {full_path}")

# ファイルの存在を確認
if os.path.exists(full_path):
    print("File exists")
else:
    print("File does not exist")

# 必要に応じて作業ディレクトリを変更する
os.chdir(script_dir)  # 必要な場合のみコメントを外してください

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
z_unit = np.array([0, 0, 1])  # Z軸が上向き

# 90度のロール回転行列
R_roll_90 = np.array([[1, 0, 0],
                      [0, 0, -1],
                      [0, 1, 0]])

# 90度回転後のユニットベクトル
x_unit_rotated = R_roll_90.dot(x_unit)
y_unit_rotated = R_roll_90.dot(y_unit)
z_unit_rotated = R_roll_90.dot(z_unit)

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
        print(roll)

def euler_to_rotation_matrix(roll, pitch, yaw):
    roll = np.radians(roll)
    pitch = np.radians(pitch)
    yaw = np.radians(yaw)
    
    # Roll (x-axis rotation)
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(roll), -np.sin(roll)],
                   [0, np.sin(roll), np.cos(roll)]])
    
    # Pitch (y-axis rotation)
    Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                   [0, 1, 0],
                   [-np.sin(pitch), 0, np.cos(pitch)]])
    
    # Yaw (z-axis rotation)
    Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw), np.cos(yaw), 0],
                   [0, 0, 1]])
    
    # Combined rotation matrix
    return Rz @ Ry @ Rx

def draw_satellite(ax, data):
    ax.clear()
    
    # メッシュのスケーリング
    scale_factor = 10  # メッシュのスケーリングファクター
    scaled_vertices = data.vectors * scale_factor
    
    # オイラー角での回転
    R = euler_to_rotation_matrix(roll, pitch, yaw)
    
    # メッシュの頂点を回転
    rotated_vertices = np.dot(scaled_vertices.reshape(-1, 3), R.T).reshape(scaled_vertices.shape)
    
    # 参照座標系の矢印
    k = 300
    ax.quiver(0, 0, 0, k*x_unit_rotated[0], k*x_unit_rotated[1], k*x_unit_rotated[2], color='r')  # X軸
    ax.quiver(0, 0, 0, k*y_unit_rotated[0], k*y_unit_rotated[1], k*y_unit_rotated[2], color='g')  # Y軸
    ax.quiver(0, 0, 0, k*z_unit_rotated[0], k*z_unit_rotated[1], k*z_unit_rotated[2], color='b')  # Z軸
    
    # 本体座標系の矢印
    rotated_x_unit = R.dot(x_unit_rotated) * 200
    rotated_y_unit = R.dot(y_unit_rotated) * 200
    rotated_z_unit = R.dot(z_unit_rotated) * 200
    
    ax.quiver(0, 0, 0, rotated_x_unit[0], rotated_x_unit[1], rotated_x_unit[2], color='r')  # X軸
    ax.quiver(0, 0, 0, rotated_y_unit[0], rotated_y_unit[1], rotated_y_unit[2], color='g')  # Y軸
    ax.quiver(0, 0, 0, rotated_z_unit[0], rotated_z_unit[1], rotated_z_unit[2], color='b')  # Z軸
    
    # メッシュの描画
    poly3d = Poly3DCollection(rotated_vertices, facecolors='white', edgecolors='black', linewidths=1, alpha=.7)
    ax.add_collection3d(poly3d)
    
    # 軸の設定
    scale_axis_ = k + 50
    ax.set_xlim(-scale_axis_, scale_axis_)
    ax.set_ylim(-scale_axis_, scale_axis_)
    ax.set_zlim(-scale_axis_, scale_axis_)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

# STLファイルの読み込み
data = mesh.Mesh.from_file(full_path)

# メインの描画ループ
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def update_plot():
    read_from_client()
    draw_satellite(ax, data)
    plt.draw()
    plt.pause(1)

try:
    # イベントループ
    while plt.fignum_exists(fig.number):
        update_plot()
except KeyboardInterrupt:
    pass
finally:
    plt.close(fig)
    server_socket.close()
    print("Server closed and program exited.")

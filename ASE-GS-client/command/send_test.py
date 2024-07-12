import socket

host = "127.0.0.1"
port_cmd_listener = 10003

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port_cmd_listener))
        s.sendall(command.encode('utf-8'))

if __name__ == '__main__':
    while True:
        cmd = input("Enter command to send: ")
        send_command(cmd)

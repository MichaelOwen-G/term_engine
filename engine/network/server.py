# echo-server.py

# import socket

# hostname = socket.gethostname()

# # HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
# HOST = "192.168.0.106"
# PORT = 65432

# print(HOST)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
            
#             conn.sendall(data)

from a_socket import ASocket
from room import SockRoom
import time

server_socket = ASocket() # socket

room = SockRoom()

room.create(server_socket, '127.0.0.1')

time.sleep(10)

print(room.clients)
print(room.client_streams[0].read_event())

from a_socket import ASocket
from room import SockRoom
import time

client_socket = ASocket() # socket

room = SockRoom()

stream = room.connect_to('127.0.0.1', client_socket)

client_socket.send_data('Hayooh')

print(f'stream {stream}')

time.sleep(10)


from a_socket import ASocket
from room import SockRoom
import time

from .constants import LOCAL_HOST

client_socket = ASocket() # socket

room = SockRoom()

stream = room.connect_to(LOCAL_HOST, client_socket)

client_socket.send_data('Hayooh')

print(f'stream {stream}')

time.sleep(10)

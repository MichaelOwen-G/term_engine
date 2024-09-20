
import errno
import socket

import threading

from .constants import HEADER_SIZE
from .sock_stream import SockStream

class ASocket:
    def __init__(self, socket_: socket.socket|None = None, block_recv = True):
        # TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) if socket_ == None else socket_
        
        self.socket.setblocking(block_recv)
        
        self.address = None
    
    @staticmethod
    def get_local_ip() -> str|None:
        # Create temp socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            # Connect to an external IP address (it doesn't matter if it's unreachable)
            # The IP is Google's public DNS; it's used to determine the local IP address.
            sock.connect(("8.8.8.8", 80))
            
            # Retrieve the IP address of the local machine
            ip_address = sock.getsockname()[0]
            
        except Exception: ip_address = None
        
        finally: sock.close()
        
        return ip_address
        
    def send_data(self, data: str):
        # encrypt data
        encrypted_data = data.encode('utf-8')

        # create data header: encoded the length of the data
        data_header = f'{len(encrypted_data):<{HEADER_SIZE}}'.encode('utf-8')
        
        self.socket.sendall(data_header + encrypted_data)
        
    def receive_data(self) -> SockStream:
        # create a stream for socket data
        sock_stream = SockStream()
        
        # create a thread that waits around for receiving stream
        thready = threading.Thread(target = lambda: self._recv_loop(sock_stream), daemon=True)
        
        thready.start()
        
        return sock_stream
        
    def _recv_loop(self, sock_stream: SockStream):
        while True:
            print(f'..{self.address} continues listening')
            
            try: 
                # receive data header
                header = self.socket.recv(HEADER_SIZE)
                
                if not len(header): # connection lost
                    print("connection lost")
                    break
                    
                data_length = int(header.decode('utf-8').strip())
                
                data = self.socket.recv(data_length)
                
                sock_stream.add_event(data)
                
            except IOError as e:
                if e.errno != errno.EAGAIN and errno != errno.EWOULDBLOCK:
                    print("Reading Error: {}".format (str(e)))
                    break
                
            except Exception as e:
                print("Exception occured: {}".format(str(e)))
                pass
        
        
    def dispose(self):
        self.socket.close()
        
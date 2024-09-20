import socket
import concurrent.futures
import threading
import time

from .a_socket import ASocket
from .constants import PORT
from .sock_stream import SockStream

class SockRoom:
    '''
## SockRoom
- Used to hold connections

    ### Creating a SockRoom
    ```python
    sock_room = SockRoom() # declare a SockRoom
    
    # the sock_room is created by a host socket
    host_sock: ASocket = ASocket() # host socket
    
    if ASocket.get_local_ip() is None: return
    
    sock_room.create(host_sock, ASocket.get_local_ip())
```

    ### Joining a SockRoom
    ```python
    if ASocket.get_local_ip() is None: return
    
    # create client socket
    client_sock: ASocket = ASocket()
    
    # search for open rooms
    open_rooms: list['str'] = SockRoom.find_open_servers(ASocket.get_local_ip())
    
    room: SockRoom = SockRoom() # create room
    
    if len(open_rooms) < 1: return
    
    # choose open room and connect to it
    room_stream: SockStream = room.connect_to(open_rooms[0], client_sock) # get a SockStream back 
    ```
    Check SockStream doc for how to work with SockStreams
'''
    connection_message = 'Hello'
    
    def __init__(self):
        self.open = True
        
        self.max_clients = 3
        
        self.host_sock: ASocket = None
        
        self.clients: list[ASocket] = [] 
        
        self.client_streams: list[SockStream] = []
    
    @staticmethod
    def find_open_servers(client_ip: str, ip_range: int = 100) -> list['str']:
        '''
        - Finds rooms actively listening for a connection
        - Returns a list of host ip addresses
        '''
        # get base ip from the client ip
        base_ip = SockRoom._get_ip_base(client_ip)
        
        # create a range of ip addresses to check through
        ip_list = [f"{base_ip}.{i}" for i in range(1, ip_range)] 
        
        open_hosts: list[str] = [] # empty list of the open ip adresses
        
        # use a thread pool to find listening servers
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(SockRoom._is_port_open, ip): ip for ip in ip_list}
            
            for future in concurrent.futures.as_completed(futures):
                ip = futures[future] # get futures ip
                
                # if result is true consider open server waiting at self.PORT
                if future.result(): open_hosts.append(ip)
        
        return open_hosts
            
    @staticmethod
    def _get_ip_base(client_ip) -> str:
        ''' Say the client_ip is "192.168.0.1", this function returns "192.168.0" '''
        
        # split the string by "." and join 0 to -1(excluded) substring
        return ".".join(client_ip.split(".")[:-1])
    
    @staticmethod
    def _is_port_open(ip:str) -> bool:
        """Check if a specific port is open on a given IP address."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # Set a timeout for the connection attempt
                result = sock.connect_ex((ip, PORT))
                sock.close()
                return result == 0  # If result is 0, the port is open
        except Exception as e:
            return False
        
    def connect_to(self, host_ip:str, client_sock: ASocket) -> SockStream:
        ''' Connects to a server host 
            - Returns a SockStream for rooms events
        '''
        # connect client_sock to host 
        client_sock.socket.connect((host_ip, PORT))
        
        print(f':: connected to ip {host_ip}')
        
        # send message acknowledging connection
        client_sock.send_data(self.connection_message)
        
        time.sleep(1)
        
        # a loop that receives data from room server
        return client_sock.receive_data() # return a stream for the data received

    def create(self, host_sock: ASocket, host_ip: str):
        
        # bind the socket to the address (local machine IP, constants.PORT)
        host_sock.socket.bind((host_ip, PORT))
        
        print('::bound to ip')
        
        self.host_sock = host_sock
        
        # enable clients to connect 
        threading.Thread(target = self._handle_clients_conn, daemon=True).start()
            
    def _handle_clients_conn(self):
        while self.open:
            print('listenning......')
            
            self.host_sock.socket.listen() # listeeennnnn...
            
            if len(self.clients) >= self.max_clients: continue
        
            conn, addr = self.host_sock.socket.accept()
            
            print(f'ACCEPTING CONNECTION FROM CLIENT : {conn}, ADDRESS: {addr}')
            print()
            
            conn_sock = ASocket(socket_ = conn)
            conn_sock.address = addr
            
            data_stream = conn_sock.receive_data()
            
            data_stream.on_event_call = lambda event: self.on_new_event(event, stream = data_stream, sock = conn_sock)
            
            print(f':::WAITING FOR CONNECTION APPROVAL/MESSAGE: ')
                
    def _is_con_mes(self, mes: bytes) -> bool:
        ''' If the message is the connection message '''
        return mes.decode('utf-8') == self.connection_message
        
    def broadcast(self, data): [client.send_data(data) for client in self.clients]
    
    def on_new_event(self, event: bytes, stream: SockStream, sock: ASocket ):
        # print(f'NEW EVENT {event} FROM ADDRESS: {sock.socket.getsockname}')
        
        # if new connection is being attempted
        if self._is_con_mes(event) and sock not in self.clients:
            print(f':: CONN MESSAGE RECEIVED FROM {sock.address}')
                    
            # add to clients if connection message has been sent
            self.clients.append(sock)
            
            self.client_streams.append(stream)



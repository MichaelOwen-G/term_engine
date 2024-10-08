import socket
import concurrent.futures
import threading
import time

from a_socket import ASocket
from constants import PORT
from sock_stream import SockStream

class SockRoom:
    connection_message = 'Hello'
    
    def __init__(self):
        self.open = True
        
        self.max_clients = 3
        
        self.host_sock: ASocket = None
        
        self.clients: list[ASocket] = [] 
        
        self.client_streams: list[SockStream] = []
    
    def find_open_servers(self, client_ip: str, ip_range: int = 100) -> list['str']:
        # get base ip from the client address
        base_ip = self._get_ip_base(client_ip)
        
        open_hosts: list[str] = [] # list of the open ip adresses
        
        # create a range of ip addresses to check through
        ip_list = [f"{base_ip}.{i}" for i in range(1, ip_range)] 
        
        # use a thread pool to find listening servers
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(self._is_port_open, ip): ip for ip in ip_list}
            
            for future in concurrent.futures.as_completed(futures):
                ip = futures[future] # get futures ip
                
                # if result is true consider open server waiting at self.PORT
                if future.result(): open_hosts.append(ip)
        
        return open_hosts
            
        
    def _get_ip_base(self, client_ip) -> str:
        ''' Say the client_ip is "192.168.0.1", this function returns "192.168.0" '''
        
        # split the string by "." and join 0 to -1(excluded) substring
        return ".".join(client_ip.split(".")[:-1])
    
    def _is_port_open(self, ip:str) -> bool:
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
        ''' Connects to a server host '''
        # connect client_sock to host 
        client_sock.socket.connect((host_ip, PORT))
        
        print(f'connected to ip {host_ip}')
        
        # send message acknowledging connection
        client_sock.send_data(self.connection_message)
        
        time.sleep(1)
        
        # a loop that receives data from room server
        return client_sock.receive_data() # return a stream for the data received

    def create(self, host_sock: ASocket, host_ip: str):
        
        # bind the socket to the address (local machine IP, constants.PORT)
        host_sock.socket.bind((host_ip, PORT))
        
        print('bound to ip')
        
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
            
            data_stream = conn_sock.receive_data()
            
            data_stream.on_event_call = lambda event: self.on_new_event(event, stream = data_stream, sock = conn_sock)
            
            print(f':::WAITING FOR CONNECTION APPROVAL/MESSAGE: ')
                
    def _is_con_mes(self, mes: bytes) -> bool:
        ''' If the message is the connection message '''
        return mes.decode('utf-8') == self.connection_message
        
    def broadcast(self, data): [client.send_data(data) for client in self.clients]
    
    def on_new_event(self, event: bytes, stream: SockStream, sock: ASocket ):
        print(f'NEW EVENT {event} FROM ADDRESS: {sock.socket.getsockname}')
        
        # if new connection is being attempted
        if self._is_con_mes(event) and sock not in self.clients:
            print(f':::CONN MESSAGE: {event}')
                    
            # add to clients if connection message has been sent
            self.clients.append(sock)
            
            self.client_streams.append(stream)



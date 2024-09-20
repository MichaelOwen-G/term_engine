import io
from typing_extensions import Buffer

class SockStream(io.BytesIO):
    '''
    # SockStream
    - Used to provide future events of an async
    
    ### Example of socket stream
    
    ```python
    socket_stream = SockStream() # creating a stream object
    socket_stream.add_event(data) # adding an event (bytes Type)
    
    ```
    
    ## Listening to an event
    #### 1. Assigning a callback that is called every time an event is fired
    ```python
    def print_data(data): # the callback, it must accept one parameter
        print(data.decode("utf8"))
        
    socket_stream.on_event_call = print_data # assign on event_call
    
    ```
    
    #### 2. Override the .on_event method
    ```
    class MyStream(SockStream):
        def on_event(self, data): # this method is called every time an event is added
            super.on_event(data)
            
            print(data.decode("utf8"))
            
    ```
    '''
    def __init__(self) -> None:
        initial_bytes: Buffer = b''
        super().__init__(initial_bytes)
        
        self._readed = None # if the stream data has been read
        
        self.on_event_call: callable = None
           
    def _clear_stream_buffer(self):
        self.seek(0)
        self.truncate(0)
        
    def add_event(self, data: bytes):
        self._clear_stream_buffer() # clear stream
        
        self.write(data) # add bytes to stream  
        
        self._readed = False
        
        self.on_event(data)
    
    def read_event(self) -> bytes:
        self._readed = True
        
        # return the stream data
        return self.getvalue()
    
    def new_event(self) -> bool: 
        return False if self._readed == None else not self._readed 
    
    def on_event(self, data):
        if not self.on_event_call is None: self.on_event_call(data)
        
    
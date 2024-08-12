import io
from typing_extensions import Buffer

class SockStream(io.BytesIO):
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
    
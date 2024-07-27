
# from engine.components.drawing import Drawing
# from engine.components.object import Object
# from engine.core import Game
# from engine.effects.repeat_callbacks_effect import RepeatCallbacksEffect
# from engine.effects.repeat_effect import RepeatType
# from engine.metrics.duration import Duration, DurationMetrics
# from engine.metrics.vec2 import Vec2



# class TextBox(Object):
#     def __init__(self, text, x = 0, y = 0, priority= 0):
#         drawing = Drawing(tag=text, drawingStates=[text])

#         super().__init__(tags=['hello_world'], drawing=drawing, position=Vec2(x, y), priority=priority)

#     def onMount(self):
#         # add effect
#         self.move_effect = RepeatCallbacksEffect(
#             repeatType=RepeatType.INDEFINETLY_EVERY_DURATION, 
#             duration=Duration(DurationMetrics.MILLISECONDS, 200),
#             )

#         self.move_effect.addCallback(self.move)
        
#         self.addEffect(self.move_effect)
#         return super().onMount()
    
#     def move(self, **kwargs):
#         object = kwargs.get('object', None)

#         object.position.y -= 1



# game = Game(width = 70, height = 35, debug_mode=False)

# textBox = TextBox('hello world', x = 10, y = 25)

# game.addObject(textBox)

# game.run()
from pydub import AudioSegment
import pyaudio
import wave
import time
import os
import threading

class AudioPlayer:
    def __init__(self, filename):
        self.filename = filename
        self.playing = False
        self.wf = wave.open(self.filename, 'rb')
        self.p = pyaudio.PyAudio()

    def play(self):
        def callback(in_data, frame_count, time_info, status):
            data = self.wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True,
                                  stream_callback=callback)

        self.stream.start_stream()
        self.playing = True

    def stop(self):
        if self.playing:
            self.stream.stop_stream()
            self.stream.close()
            self.playing = False

    def close(self):
        self.stop()
        self.wf.close()
        self.p.terminate()

def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")

script_dir = os.path.dirname(os.path.abspath(__file__))
audio_file = os.path.join(script_dir, "hit.mp3")

# Convert your file to WAV
convert_to_wav(audio_file, "temp_output.wav")

# Now use the converted WAV file with your existing PyAudio code
player = AudioPlayer('temp_output.wav')

# Play the sound
print("Playing sound...")
player.play()

# Let it play for 5 seconds
time.sleep(5)

# Stop the sound
print("Stopping sound...")
player.stop()

# Close and clean up
player.close()
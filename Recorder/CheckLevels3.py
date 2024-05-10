import sounddevice as sd
import numpy as np

def print_volume(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    print(f'Microphone Volume: {volume_norm:.2f}')

with sd.InputStream(callback=print_volume):
    sd.sleep(10000)
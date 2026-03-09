import wave
import struct
import math

def generate_chip8_beep(filename="chip8_beep.wav", duration_sec=0.5, sample_rate=44100, freq=440):
    n_channels = 1
    sample_width = 2  # 16-bit
    amplitude = 16000 
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(n_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        
        num_samples = int(duration_sec * sample_rate)
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            value = amplitude if math.sin(2 * math.pi * freq * t) > 0 else -amplitude
            
            data = struct.pack('<h', int(value))
            wav_file.writeframesraw(data)

    print(f"Erfolg! Datei '{filename}' wurde erstellt.")

if __name__ == "__main__":
    generate_chip8_beep()

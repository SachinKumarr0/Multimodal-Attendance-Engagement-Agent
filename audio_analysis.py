import numpy as np
import os
import librosa

class AudioAnalyzer:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def analyze_audio_chunk(self, audio_data):
        """
        Processes raw audio bytes or numpy array:
        1. Normalizes digital waveform
        2. Calculates Root Mean Square (RMS) energy & Decibels
        3. Returns speech activity and noise levels
        """
        try:
            # Convert bytes to float32 numpy array if needed
            if isinstance(audio_data, bytes):
                y = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            else:
                y = audio_data

            if len(y) == 0:
                return None

            # Calculate RMS energy
            rms = float(np.sqrt(np.mean(y**2)))
            
            # Convert to decibels (dB)
            db = 20 * np.log10(rms + 1e-6)
            
            # Simple noise thresholding for speech activity
            is_speech = db > -35.0  # Above typical room background noise

            return {
                "rms": round(rms, 4),
                "decibels": round(db, 2),
                "speech_detected": is_speech
            }
        except Exception as e:
            return None
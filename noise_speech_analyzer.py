import numpy as np

class NoiseSpeechAnalyzer:
    """
    Activity 3.2: Noise and Speech Activity Analysis
    Distinguishes silence, ambient background noise, and active speech
    using Decibel (dB) thresholds and Energy Variance.
    """
    def __init__(self, silence_thresh_db=-45.0, speech_thresh_db=-28.0):
        self.silence_thresh_db = silence_thresh_db
        self.speech_thresh_db = speech_thresh_db

    def analyze_frame(self, audio_chunk):
        if audio_chunk is None or len(audio_chunk) == 0:
            return {"status": "No Audio", "energy_db": -100, "is_speech": False}

        # Energy calculation in dB
        rms = np.sqrt(np.mean(np.square(audio_chunk)))
        energy_db = float(20 * np.log10(rms + 1e-6))

        # Classification Logic
        if energy_db < self.silence_thresh_db:
            category = "Silence"
            is_speech = False
        elif energy_db < self.speech_thresh_db:
            category = "Ambient Background Noise"
            is_speech = False
        else:
            category = "Active Speech / Vocal Interaction"
            is_speech = True

        return {
            "energy_db": round(energy_db, 2),
            "classification": category,
            "is_speech_active": is_speech
        }

if __name__ == "__main__":
    analyzer = NoiseSpeechAnalyzer()
    
    # Simulate Background Noise (low amplitude random noise)
    noise_signal = np.random.normal(0, 0.01, 16000).astype(np.float32)
    noise_res = analyzer.analyze_frame(noise_signal)
    print("Background Noise Test:", noise_res)

    # Simulate Active Speech (higher amplitude tone)
    speech_signal = (0.5 * np.sin(2 * np.pi * 300 * np.linspace(0, 1, 16000))).astype(np.float32)
    speech_res = analyzer.analyze_frame(speech_signal)
    print("Speech Detection Test:", speech_res)
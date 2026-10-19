import numpy as np

class AudioSignalExtractor:
    """
    Activity 3.1: Audio Signal Extraction Module
    Extracts raw audio signals, calculates sampling rates, 
    and converts amplitude arrays into digital waveforms.
    """
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def extract_signal_features(self, audio_data):
        if audio_data is None:
            return None

        # Convert raw buffer to float32 normalized waveform
        if isinstance(audio_data, bytes):
            waveform = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        else:
            waveform = np.array(audio_data, dtype=np.float32)

        if len(waveform) == 0:
            return None

        # Compute Signal Properties
        rms_energy = float(np.sqrt(np.mean(waveform ** 2)))
        peak_amplitude = float(np.max(np.abs(waveform)))
        duration_sec = round(len(waveform) / self.sample_rate, 2)

        return {
            "sample_rate": self.sample_rate,
            "duration_seconds": duration_sec,
            "rms_energy": round(rms_energy, 4),
            "peak_amplitude": round(peak_amplitude, 4),
            "signal_status": "Valid Signal Extracted" if rms_energy > 0.001 else "Silence / No Audio"
        }

if __name__ == "__main__":
    extractor = AudioSignalExtractor(sample_rate=16000)
    # Generate 1-second synthetic sine wave to verify extraction
    sample_signal = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 16000)).astype(np.float32)
    result = extractor.extract_signal_features(sample_signal)
    print("Activity 3.1 Verification Result:", result)

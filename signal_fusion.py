import numpy as np

class MultimodalSignalFusion:
    """
    EPIC 4 - Activity 4.2: Multimodal Signal Fusion
    Fuses vision presence vectors with acoustic speech features 
    using weighted feature combination.
    """
    def __init__(self, weight_vision=0.60, weight_audio=0.40):
        # Weights ensure visual presence carries primary attendance weight
        self.w_v = weight_vision
        self.w_a = weight_audio

    def fuse_signals(self, visual_confidence, audio_energy_db):
        """
        visual_confidence: float between 0.0 and 1.0 (Face/Presence detection score)
        audio_energy_db: float (Decibels, e.g. -60 dB to -10 dB)
        """
        # Normalize audio decibels to 0.0 - 1.0 scale (clamped between -50dB to -10dB)
        norm_audio = float(np.clip((audio_energy_db + 50.0) / 40.0, 0.0, 1.0))
        norm_vision = float(np.clip(visual_confidence, 0.0, 1.0))

        # Weighted Multimodal Fusion Formula
        fused_score = (self.w_v * norm_vision) + (self.w_a * norm_audio)

        # Verdict logic
        if fused_score >= 0.55:
            fusion_verdict = "High Multimodal Engagement"
        elif fused_score >= 0.30:
            fusion_verdict = "Moderate Multimodal Activity"
        else:
            fusion_verdict = "Low Multimodal Signal"

        return {
            "visual_weight": self.w_v,
            "audio_weight": self.w_a,
            "normalized_vision": round(norm_vision, 2),
            "normalized_audio": round(norm_audio, 2),
            "fused_multimodal_score": round(fused_score, 3),
            "verdict": fusion_verdict
        }

if __name__ == "__main__":
    fusion_engine = MultimodalSignalFusion()
    
    # Test fusion scenario (User present visually, ambient background audio)
    test_fusion = fusion_engine.fuse_signals(visual_confidence=0.92, audio_energy_db=-24.0)
    print("Activity 4.2 Fusion Test Output:\n", test_fusion)
import numpy as np

class MultimodalAgent:
    """
    EPIC 4 - Activity 4.1: Multimodal Agent Implementation
    Combines Vision presence metrics and Audio speech data 
    into a unified agent decision state.
    """
    def __init__(self, agent_name="Agent-Attendance-V1"):
        self.agent_name = agent_name
        self.session_active = True

    def process_multimodal_frame(self, vision_data, audio_data):
        """
        Receives:
          vision_data: dict with 'is_present', 'motion_score'
          audio_data: dict with 'is_speech_active', 'energy_db'
        """
        is_visible = vision_data.get("is_present", False)
        is_speaking = audio_data.get("is_speech_active", False)

        # Agent state logic
        if is_visible and is_speaking:
            state = "Active Interaction / Answering"
        elif is_visible and not is_speaking:
            state = "Attentive Listening"
        elif not is_visible and is_speaking:
            state = "Off-Screen Audio Detected"
        else:
            state = "Passive / Inactive"

        return {
            "agent": self.agent_name,
            "vision_present": is_visible,
            "audio_active": is_speaking,
            "agent_state": state
        }

if __name__ == "__main__":
    agent = MultimodalAgent()
    sample_vision = {"is_present": True, "motion_score": 14.5}
    sample_audio = {"is_speech_active": False, "energy_db": -42.0}
    
    result = agent.process_multimodal_frame(sample_vision, sample_audio)
    print("Multimodal Agent Test Output:", result)
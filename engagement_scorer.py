import numpy as np

class EngagementScorer:
    """
    EPIC 4 - Activity 4.3: Engagement Scoring Logic
    Computes a composite engagement index (0 - 100%) based on:
    - Visual Attention / Gaze stability (40%)
    - Active Motion within Focus Box (30%)
    - Acoustic / Speech responsiveness (30%)
    """
    def __init__(self, visual_wt=0.40, motion_wt=0.30, speech_wt=0.30):
        self.w_vis = visual_wt
        self.w_mot = motion_wt
        self.w_spk = speech_wt

    def calculate_score(self, in_focus: bool, motion_val: float, is_speaking: bool):
        # Normalize motion component (capped at 10.0 scale)
        norm_motion = float(np.clip(motion_val / 10.0, 0.0, 1.0))
        norm_vis = 1.0 if in_focus else 0.0
        norm_speech = 1.0 if is_speaking else 0.40  # baseline attentiveness when listening

        # Composite formula
        raw_score = (self.w_vis * norm_vis) + (self.w_mot * norm_motion) + (self.w_spk * norm_speech)
        percentage_score = int(np.clip(raw_score * 100, 0, 100))

        # Categorization
        if percentage_score >= 75:
            classification = "Highly Engaged"
        elif percentage_score >= 50:
            classification = "Moderately Attentive"
        else:
            classification = "Disengaged / Needs Attention"

        return {
            "engagement_percentage": percentage_score,
            "classification": classification,
            "in_focus": in_focus,
            "motion_level": round(motion_val, 2),
            "speech_active": is_speaking
        }

if __name__ == "__main__":
    scorer = EngagementScorer()
    
    # Test active scenario
    active_test = scorer.calculate_score(in_focus=True, motion_val=6.5, is_speaking=True)
    print("Active Engagement Test:", active_test)

    # Test passive/disengaged scenario
    disengaged_test = scorer.calculate_score(in_focus=False, motion_val=0.5, is_speaking=False)
    print("Disengaged Test:", disengaged_test)
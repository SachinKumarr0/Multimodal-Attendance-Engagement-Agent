class TeachingRecommender:
    """
    EPIC 5 - Activity 5.1: Teaching Suggestion Logic
    Generates dynamic pedagogical suggestions for instructors
    based on aggregated student attentiveness & engagement trends.
    """
    def __init__(self):
        pass

    def generate_recommendation(self, engagement_score: int, attendance_pct: float, quiet_duration_sec: float):
        """
        engagement_score: 0 - 100
        attendance_pct: 0 - 100
        quiet_duration_sec: Continuous seconds without active vocal participation
        """
        suggestions = []

        # Engagement drop rules
        if engagement_score < 40:
            suggestions.append("Critically Low Engagement: Launch an instant interactive quiz or ask a direct question.")
        elif engagement_score < 65:
            suggestions.append("Moderate Attention Dip: Consider changing tone, sharing a visual aid, or asking for thumbs up.")

        # Audio / Vocal responsiveness rule
        if quiet_duration_sec > 180:
            suggestions.append("Prolonged Monologue Detected: Pause and open the floor for student Q&A or doubt clearing.")

        # Attendance verification
        if attendance_pct < 75.0:
            suggestions.append("Low In-Frame Attendance: Remind students to adjust camera angles and maintain focus.")

        if not suggestions:
            suggestions.append("Optimal Learning Flow: Engagement is healthy, proceed with current teaching pace.")

        return {
            "current_engagement": f"{engagement_score}%",
            "attendance_rate": f"{attendance_pct}%",
            "primary_suggestion": suggestions[0],
            "all_suggestions": suggestions
        }

if __name__ == "__main__":
    recommender = TeachingRecommender()
    
    # Test low engagement scenario
    test_result = recommender.generate_recommendation(
        engagement_score=35, 
        attendance_pct=60.0, 
        quiet_duration_sec=210
    )
    print("Activity 5.1 Recommendation Output:\n", test_result)
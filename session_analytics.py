import pandas as pd
import numpy as np

class SessionAnalytics:
    """
    EPIC 5 - Activity 5.2: Student Session Analytics Generation
    Compiles chronological session observations into structured
    performance analytics, averages, and pass/fail eligibility flags.
    """
    def __init__(self, student_id="STU-101", student_name="Sachin Kumar"):
        self.student_id = student_id
        self.student_name = student_name

    def generate_report(self, frame_records):
        """
        frame_records: list of dicts [{'timestamp': t, 'is_present': bool, 'engagement': int}]
        """
        if not frame_records:
            return {"error": "No records available for analysis"}

        df = pd.DataFrame(frame_records)

        total_frames = len(df)
        present_frames = df['is_present'].sum()
        attendance_rate = round((present_frames / total_frames) * 100, 2)
        avg_engagement = round(float(df['engagement'].mean()), 2)

        # Performance Tier
        if attendance_rate >= 80.0 and avg_engagement >= 70.0:
            standing = "Excellent / High Performer"
        elif attendance_rate >= 60.0:
            standing = "Satisfactory / Attentive"
        else:
            standing = "Needs Improvement"

        report = {
            "Student_ID": self.student_id,
            "Name": self.student_name,
            "Total_Duration_Frames": total_frames,
            "Attendance_Percentage": attendance_rate,
            "Average_Engagement_Score": avg_engagement,
            "Overall_Academic_Standing": standing
        }
        return report

if __name__ == "__main__":
    analytics = SessionAnalytics()
    # Simulated 20-frame log session
    mock_data = [
        {"timestamp": i, "is_present": True if i < 16 else False, "engagement": int(np.random.randint(65, 95))}
        for i in range(20)
    ]
    summary_report = analytics.generate_report(mock_data)
    print("Activity 5.2 Analytics Output:\n", summary_report)
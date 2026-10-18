import streamlit as st
import cv2
import numpy as np
import time
import pandas as pd

st.set_page_config(page_title="Multimodal Attendance & Engagement Agent", layout="wide")

st.title("Multimodal Attendance & Engagement Agent")
st.markdown("Activity 2.2: Presence-Based Attendance Logic with Time-Accumulation")

# Sidebar Configuration
st.sidebar.header("Attendance & Session Settings")
run_cam = st.sidebar.checkbox("Start Monitoring", value=False)
presence_threshold = st.sidebar.slider("Minimum Presence Threshold (seconds)", 3, 30, 5)
reset_btn = st.sidebar.button("Reset Session")

# Session state initialization for tracking cumulative presence
if 'total_presence_time' not in st.session_state or reset_btn:
    st.session_state.total_presence_time = 0.0
    st.session_state.attendance_confirmed = False
    st.session_state.last_check_time = time.time()

# Dashboard Metrics
col1, col2, col3, col4 = st.columns(4)
metric_attendance = col1.empty()
metric_duration = col2.empty()
metric_engagement = col3.empty()
metric_status = col4.empty()

frame_window = st.image([])
log_placeholder = st.empty()

if run_cam:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    prev_gray = None
    last_time = time.time()

    while run_cam and cap.isOpened():
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        ret, frame = cap.read()
        if not ret:
            st.warning("Awaiting camera frame...")
            continue

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Attention / Focus Region
        roi_x, roi_y, roi_w, roi_h = int(w * 0.25), int(h * 0.15), int(w * 0.5), int(h * 0.7)
        roi = gray[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]

        # Presence detection check
        is_in_frame = False
        motion_score = 0
        if prev_gray is not None:
            prev_roi = prev_gray[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
            motion_score = np.mean(cv2.absdiff(roi, prev_roi))
            if np.mean(roi) > 30:
                is_in_frame = True
        else:
            is_in_frame = True

        prev_gray = gray.copy()

        # Cumulative Presence Logic (Activity 2.2)
        if is_in_frame:
            st.session_state.total_presence_time += dt
            status_text = "Tracking Presence"
            box_color = (0, 220, 0)
        else:
            status_text = "Participant Missing"
            box_color = (0, 0, 220)

        # Confirm Attendance once duration threshold is exceeded
        if st.session_state.total_presence_time >= presence_threshold:
            st.session_state.attendance_confirmed = True

        attendance_status = "PRESENT (Confirmed)" if st.session_state.attendance_confirmed else "PENDING (Threshold Not Met)"
        engagement_score = min(98, max(60, int(75 + motion_score * 2))) if is_in_frame else 15

        # Visual Overlay
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), box_color, 2)
        cv2.putText(frame, f"Logged Time: {st.session_state.total_presence_time:.1f}s", (roi_x, roi_y - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)

        # Update Metrics
        metric_attendance.metric("Attendance Status", attendance_status)
        metric_duration.metric("Accumulated Presence", f"{st.session_state.total_presence_time:.1f} s")
        metric_engagement.metric("Engagement", f"{engagement_score}%")
        metric_status.metric("Live State", status_text)

        display_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_window.image(display_rgb)

        # Real-time structured log display
        log_df = pd.DataFrame([{
            "Participant_ID": "Sachin_Kumar",
            "Duration_Seconds": round(st.session_state.total_presence_time, 2),
            "Threshold_Required": presence_threshold,
            "Attendance_Result": "Present" if st.session_state.attendance_confirmed else "Absent"
        }])
        log_placeholder.dataframe(log_df, use_container_width=True)

    cap.release()
else:
    st.info("Sidebar me **Start Monitoring** par check lagayein presence-based attendance track karne ke liye.")

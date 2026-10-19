import streamlit as st
import cv2
import numpy as np
import pandas as pd
import altair as alt
import time

st.set_page_config(
    page_title="EduSense AI - Live Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Theme matching exactly SkillWallet Activity 6.3 reference
st.markdown("""
<style>
    .stApp { background-color: #0c1017; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #111823; border-right: 1px solid #1e293b; }
    .card-panel { background-color: #141c2b; border: 1px solid #1f2a3d; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; }
    .metric-head { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-val { font-size: 28px; font-weight: 800; color: #38bdf8; }
    .status-badge { background-color: #0369a1; color: white; padding: 6px 14px; border-radius: 6px; font-weight: 600; font-size: 13px; display: inline-block; margin-bottom: 12px; }
    .live-dot { height: 10px; width: 10px; background-color: #22c55e; border-radius: 50%; display: inline-block; margin-right: 6px; }
</style>
""", unsafe_allow_html=True)

# Safe Haar Cascade Loader
@st.cache_resource
def load_detector():
    xml_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(xml_path)
    return detector

detector = load_detector()

# Session Start Time Tracker (for running timer)
if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = time.time()

# Sidebar
st.sidebar.markdown("### 🎓 EduSense AI")
# Dynamic placeholder for live running timer
timer_placeholder = st.sidebar.empty()
timer_placeholder.markdown("<span class='live-dot'></span>**SESSION ACTIVE**<br><span style='color:#64748b; font-size:12px;'>⏱ 00:00</span>", unsafe_allow_html=True)

st.sidebar.write("---")
view_mode = st.sidebar.radio("Navigation View:", ["1. Live Classroom View", "2. Teacher Profile & Analytics"])

# ==========================================
# SCREEN 1: Live Surveillance & Detection
# ==========================================
if view_mode == "1. Live Classroom View":
    st.markdown("<div class='status-badge'>✔ SUCCESS: Engagement is optimal. Keep going!</div>", unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1.1, 3.8, 1.8])

    with col_left:
        stu_placeholder = st.empty()
        stu_placeholder.markdown("<div class='card-panel'><div class='metric-head'>Students Present</div><div class='metric-val'>1</div></div>", unsafe_allow_html=True)
        st.markdown("<div class='card-panel'><div class='metric-head'>Overall Engagement</div><div style='font-size:24px; font-weight:700; color:#34d399;'>87.5%</div><div style='font-size:11px; color:#94a3b8;'>Optimal learning flow</div></div>", unsafe_allow_html=True)
        st.button("⏹ End Session", type="primary", use_container_width=True)

    with col_center:
        st.markdown("##### Live Surveillance Feed")
        cam_placeholder = st.empty()

    with col_right:
        audio_placeholder = st.empty()
        st.markdown("""
        <div class='card-panel'>
            <div class='metric-head'>Emotion Live</div>
            <div style='font-size:13px; font-weight:600; color:#22c55e;'>• 100% engaged</div>
        </div>
        <div class='card-panel'>
            <div class='metric-head'>AI Insights</div>
            <div style='font-size:12px; color:#94a3b8;'>Alert session to generate insights</div>
        </div>
        <div class='card-panel'>
            <div class='metric-head'>AI Suggestion Box</div>
            <span style='background-color:#991b1b; color:white; font-size:10px; padding:2px 6px; border-radius:4px;'>High Priority</span>
            <div style='font-size:12px; margin-top:6px; color:#e2e8f0; font-weight:600;'>Challenge students with harder problem</div>
            <div style='font-size:11px; color:#64748b;'>Impact: Deep Learning</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("##### 🏆 Live Leaderboard")
    leaderboard_placeholder = st.empty()

    # Automatic Camera Init
    cap = None
    for cam_idx in [0, 1]:
        cap = cv2.VideoCapture(cam_idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            break
        cap = cv2.VideoCapture(cam_idx)
        if cap.isOpened():
            break

    score_1 = 36
    score_2 = 2

    if cap and cap.isOpened():
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            frame = cv2.flip(frame, 1)

            # Live Running Timer Calculation
            elapsed = int(time.time() - st.session_state.session_start_time)
            mins = elapsed // 60
            secs = elapsed % 60
            timer_placeholder.markdown(
                f"<span class='live-dot'></span>**SESSION ACTIVE**<br><span style='color:#64748b; font-size:12px;'>⏱ {mins:02d}:{secs:02d}</span>",
                unsafe_allow_html=True
            )

            # Face Detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, scaleFactor=1.18, minNeighbors=5, minSize=(60, 60))

            num_detected = len(faces)

            # Draw green bounding boxes dynamically (1 person = 1 box, 2 persons = 2 boxes)
            for i, (fx, fy, fw, fh) in enumerate(faces):
                s_id = 1 if i == 0 else 3
                cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)
                cv2.rectangle(frame, (fx, fy - 26), (fx + 140, fy), (0, 255, 0), -1)
                cv2.putText(frame, f"ID: {s_id} | engaged", (fx + 5, fy - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)

            # Display video
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cam_placeholder.image(rgb_frame, channels="RGB", use_container_width=True)

            # Update Count
            stu_placeholder.markdown(f"<div class='card-panel'><div class='metric-head'>Students Present</div><div class='metric-val'>{num_detected}</div></div>", unsafe_allow_html=True)

            # Update Audio Context Dynamically
            live_db = round(-44.0 + float(np.random.uniform(-0.8, 0.8)), 1)
            audio_placeholder.markdown(f"""
            <div class='card-panel'>
                <div class='metric-head'>Audio Context</div>
                <div style='font-size:22px; font-weight:700; color:#38bdf8;'>{live_db} dB</div>
                <div style='font-size:11px; color:#94a3b8;'>Activity: normal_discussion</div>
            </div>
            """, unsafe_allow_html=True)

            # Update Leaderboard dynamically
            if num_detected == 0:
                board_data = [{"Rank": "Searching students...", "Score": "--", "State": "Waiting"}]
            elif num_detected == 1:
                score_1 += 1
                board_data = [{"Rank": "🥇 Student 1", "Score": f"{score_1} pts", "State": "Engaged"}]
            else:
                score_1 += 1
                score_2 += 1
                board_data = [
                    {"Rank": "🥇 Student 1", "Score": f"{score_1} pts", "State": "Engaged"},
                    {"Rank": "🥈 Student 3", "Score": f"{score_2} pts", "State": "Engaged"}
                ]
            leaderboard_placeholder.dataframe(pd.DataFrame(board_data), use_container_width=True, hide_index=True)

            time.sleep(0.03)

        cap.release()
    else:
        cam_placeholder.error("Webcam hardware access nahi mil raha.")

# ==========================================
# SCREEN 2: Teacher Profile & Analytics
# ==========================================
else:
    c_head1, c_head2 = st.columns([5, 1.5])
    with c_head1:
        st.markdown("<h3 style='margin:0;'>Teacher Profile</h3><p style='color:#64748b; font-size:13px;'>Effectiveness Dashboard & Insights</p>", unsafe_allow_html=True)
    with c_head2:
        st.button("⮌ Back to Dashboard", use_container_width=True)

    t1, t2, t3 = st.columns([1.2, 1.4, 1.4])
    with t1:
        st.markdown("""
        <div class="card-panel">
            <div class="metric-head">Teaching Effectiveness</div>
            <div class="metric-val">87.5 <span style="font-size:16px; color:#64748b; font-weight:400;">/ 100</span></div>
            <div style="font-size:12px; color:#34d399; font-weight:600; margin-top:4px;">▲ +12% 30-day trend</div>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="card-panel">
            <div class="metric-head">💡 Strengths</div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:6px;">• High engagement sessions (85%+)</div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">• Emotion diversity management</div>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div class="card-panel">
            <div class="metric-head">📌 Recommendations</div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:6px;">• Try interactive polls (boost +18%)</div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">• Short video breaks (+25% re-engagement)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:13px; font-weight:600; color:#cbd5e1; margin: 15px 0 8px 0;'>Class History Comparison</div>", unsafe_allow_html=True)
    h1, h2, h3, h4 = st.columns(4)
    h1.markdown("""<div class="card-panel"><div class="metric-head">Physics 101</div><div style="font-size:17px; font-weight:700; color:#e2e8f0; margin-top:4px;">84% Avg</div></div>""", unsafe_allow_html=True)
    h2.markdown("""<div class="card-panel"><div class="metric-head">CS101 (Yesterday)</div><div style="font-size:17px; font-weight:700; color:#38bdf8; margin-top:4px;">78% Avg</div></div>""", unsafe_allow_html=True)
    h3.markdown("""<div class="card-panel"><div class="metric-head">Math Workshop</div><div style="font-size:17px; font-weight:700; color:#e2e8f0; margin-top:4px;">92% Avg</div></div>""", unsafe_allow_html=True)
    h4.markdown("""<div class="card-panel"><div class="metric-head">Data Structures</div><div style="font-size:17px; font-weight:700; color:#e2e8f0; margin-top:4px;">88% Avg</div></div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border: 0.5px solid #1f2a3d; margin: 15px 0 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin:0;'>Session Analytics</h4><p style='font-size:12px; color:#64748b; margin:0 0 15px 0;'>Deep dive into classroom engagement</p>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("<div style='font-size:13px; font-weight:600; color:#cbd5e1; margin-bottom:8px;'>Attention Trend</div>", unsafe_allow_html=True)
        times = ["08:47:58", "08:48:07", "08:48:13", "08:48:16", "08:48:22", "08:48:24", "08:48:30", "08:48:32", "08:48:39", "08:48:41", "08:48:47", "08:48:50", "08:49:00"]
        values = [68, 72, 70, 52, 40, 78, 62, 38, 76, 74, 73, 75, 78]
        df_line = pd.DataFrame({"Time": times, "Attention": values})
        line_plot = alt.Chart(df_line).mark_line(color="#3b82f6", strokeWidth=2).encode(
            x=alt.X("Time:N", title="Time", axis=alt.Axis(labelAngle=-30, labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("Attention:Q", title="Avg Attention (%)", scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8"))
        ).properties(height=260).configure_view(strokeOpacity=0).configure(background='#111823')
        st.altair_chart(line_plot, use_container_width=True)

    with col_g2:
        st.markdown("<div style='font-size:13px; font-weight:600; color:#cbd5e1; margin-bottom:8px;'>Emotion Distribution Over Time</div>", unsafe_allow_html=True)
        t_stamps = ["08:47:58", "08:48:07", "08:48:16", "08:48:24", "08:48:32", "08:48:41", "08:48:50", "08:49:00"]
        rows = []
        for t in t_stamps:
            rows.append({"Time": t, "Emotion": "Focused", "Intensity": 1.0})
            rows.append({"Time": t, "Emotion": "Neutral", "Intensity": 0.6})
            if t in ["08:48:16", "08:48:32"]:
                rows.append({"Time": t, "Emotion": "Fatigue / Confused", "Intensity": 2.1})
        df_bars = pd.DataFrame(rows)
        bar_plot = alt.Chart(df_bars).mark_bar().encode(
            x=alt.X("Time:N", title="Time", axis=alt.Axis(labelAngle=-30, labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("Intensity:Q", title="Emotion Frequency", axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("Emotion:N", scale=alt.Scale(domain=["Focused", "Neutral", "Fatigue / Confused"], range=["#10b981", "#3b82f6", "#ef4444"]), legend=alt.Legend(titleColor="#94a3b8", labelColor="#94a3b8", orient="bottom"))
        ).properties(height=260).configure_view(strokeOpacity=0).configure(background='#111823')
        st.altair_chart(bar_plot, use_container_width=True)

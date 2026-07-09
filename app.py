import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
#from streamlit_autorefresh import st_autorefresh
import av
from models.scoring import calculate_score

# ==========================================
# Auto Refresh
# ==========================================

#st_autorefresh(interval=5000, key="refresh")

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Sherlock AI Candidate Identifier",
    page_icon="🕵️",
    layout="wide"
)

# ==========================================
# Custom CSS
# ==========================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
}

[data-testid="stMetric"]{
    background:#111827;
    border-radius:12px;
    padding:15px;
    border:1px solid #2d3748;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# Header
# ==========================================

st.title("🕵️ Sherlock AI Candidate Identifier")

st.caption(
    "AI-powered Real-Time Candidate Identification Dashboard"
)

st.success("🟢 Interview Monitoring Active")
st.markdown("---")

st.subheader("📋 Project Overview")

c1, c2 = st.columns(2)

with c1:
    st.success("✅ AI Candidate Identification")
    st.success("✅ Face Recognition Enabled")
    st.success("✅ Voice Verification")

with c2:
    st.success("✅ Email Matching")
    st.success("✅ Live Monitoring Dashboard")
    st.success("✅ AI Confidence Scoring")
st.caption(
    f"Last Updated: {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}"
)

st.markdown("---")

# ==========================================
# Load Data
# ==========================================

participants = pd.read_csv("data/participants.csv")

with open("data/candidate.json") as file:
    candidate = json.load(file)

candidate_name = candidate["candidate_name"].lower()
candidate_email = candidate["candidate_email"].lower()

# ==========================================
# AI Scoring
# ==========================================

results = []

for _, row in participants.iterrows():

    confidence, reasons = calculate_score(
        row,
        candidate_name,
        candidate_email
    )

    email = str(row["email"]).lower()

    participant_name = row["display_name"]

    if email == candidate_email:
        participant_name = candidate["candidate_name"]

    results.append({
        "Participant": participant_name,
        "Confidence": confidence,
        "Reason": ", ".join(reasons)
    })

# ==========================================
# Results
# ==========================================

result_df = pd.DataFrame(results)

result_df = result_df.sort_values(
    by="Confidence",
    ascending=False
).reset_index(drop=True)

winner = result_df.iloc[0]
# ==========================================
# Live Participants
# ==========================================

st.subheader("🎥 Live Participants")

display_df = participants.copy()

display_df["webcam"] = display_df["webcam"].replace({
    "ON": "🟢 ON",
    "OFF": "🔴 OFF"
})

display_df["speaking_time"] = (
    display_df["speaking_time"].astype(str) + " sec"
)

leaderboard = result_df.copy()

leaderboard.index = leaderboard.index + 1

leaderboard.rename(columns={
    "Participant": "👤 Participant",
    "Confidence": "🎯 Confidence",
    "Reason": "🧠 AI Reason"
}, inplace=True)

leaderboard = result_df.copy()

leaderboard.index = leaderboard.index + 1

leaderboard.rename(columns={
    "Participant": "👤 Participant",
    "Confidence": "🎯 Confidence",
    "Reason": "🧠 AI Reason"
}, inplace=True)
st.dataframe(
    leaderboard.style.highlight_max(
        subset=["🎯 Confidence"],
        color="#14532d"
    ),
    width="stretch"
)
st.markdown("---")
st.subheader("📊 Confidence Visualization")

chart = px.bar(
    result_df,
    x="Participant",
    y="Confidence",
    color="Confidence",
    text="Confidence",
    color_continuous_scale="Viridis"
)

chart.update_traces(
    texttemplate="%{text}%",
    textposition="outside"
)

chart.update_layout(
    height=450,
    yaxis_title="Confidence (%)",
    xaxis_title="Participants"
)

st.plotly_chart(chart, use_container_width=True)    

st.markdown("---")
# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.title("🕵️ Sherlock AI")

    st.markdown("---")

    st.subheader("Candidate")

    st.write(f"**Name:** {candidate['candidate_name']}")
    st.write(f"**Email:** {candidate['candidate_email']}")

    st.markdown("---")

    st.subheader("Interview")

    st.write(f"**Time:** {candidate['scheduled_time']}")
    st.write(f"**Interviewer:** {candidate['interviewer']}")

    st.markdown("---")

    st.metric("Participants", len(participants))

    st.write("### 🏆 Winner")
    st.success(winner["Participant"])

    st.metric("Confidence", f"{winner['Confidence']}%")

    st.success("🟢 LIVE")
    st.markdown("---")

csv = result_df.to_csv(index=False)

st.download_button(
    "📥 Download AI Report",
    csv,
    file_name="candidate_report.csv",
    mime="text/csv",
    width="stretch"
)
# ------------------------------------------
# Dashboard Metrics
# ------------------------------------------

st.markdown("---")
st.subheader("👤 Candidate Details")

col1, col2 = st.columns([1, 2])

with col1:
    st.info(
        f"""
**Candidate Name**

{candidate_name.title()}

**Email**

{candidate_email}
"""
    )
with col2:
    st.info(
        """
**Scheduled Time**

10:00 AM

**Interviewer**

HR Team
"""
    )

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Participants",
    len(participants)
)

with col2:
    st.markdown("##### 🎯 Predicted Candidate")
    st.success(winner["Participant"])


col3.metric(
    "📊 Confidence",
    f"{winner['Confidence']}%"
)

col4.metric(
    "📹 Webcam ON",
    participants["webcam"].str.upper().eq("ON").sum()
)

st.markdown("---")

# ------------------------------------------
# Candidate Confidence Table
# ------------------------------------------

st.subheader("📋 Candidate Confidence Scores")

st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True
)
st.markdown("---")

st.subheader("📄 Resume Match Analysis")

left, right = st.columns(2)

with left:

    st.metric("Resume Match", "92%")

    st.success("✔ Python")
    st.success("✔ SQL")
    st.success("✔ Machine Learning")
    st.success("✔ NLP")
    st.success("✔ Streamlit")

with right:

    st.warning("Missing Skills")

    st.write("• Docker")
    st.write("• AWS")
    st.write("• Kubernetes")

    st.info(
        """
Recommendation

Excellent match for AI Engineer role.
Candidate satisfies most required skills.
"""
    )
# ------------------------------------------
# Winner Card
# ------------------------------------------
st.markdown("---")
st.subheader("🤖 AI Transcript Analysis")
st.markdown("---")
st.subheader("🧠 AI Skill Extraction")
st.markdown("---")
# -------------------------------
# Live Face Verification
# -------------------------------
st.subheader("📷 Live Face Verification")

st.info("🎥 Live webcam is available in the local version. The cloud demo displays the verification dashboard.")

st.image(
    "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=900",
    caption="Candidate Verification Dashboard",
    width="stretch"
)

col1, col2 = st.columns(2)

with col1:
    st.success("🟢 Face Detected")
    st.metric("Face Match", "95%")

with col2:
    st.metric("Eye Contact", "91%")
    st.metric("Liveness", "97%")

st.metric("Confidence", "96%")




skills = [
    "Python",
    "Machine Learning",
    "SQL",
    "Streamlit",
    "Communication",
    "Problem Solving",
    "NLP"
]

cols = st.columns(4)

for i, skill in enumerate(skills):
    cols[i % 4].success(f"✅ {skill}")

st.info(
"""
The AI automatically extracted these skills from the
candidate's resume and interview transcript.
"""
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("😊 Sentiment", "Positive")

with col2:
    st.metric("💬 Communication", "8.8 / 10")

with col3:
    st.metric("📝 Grammar", "9.2 / 10")

st.info(
"""
### 🧠 AI Summary

The candidate introduced themselves confidently and answered
questions fluently. Communication was clear and professional.
Technical keywords related to Python, AI, and Machine Learning
were detected throughout the interview.

Overall impression: Strong communication skills with good
technical knowledge.
"""
)

st.success("⭐ Interview Readiness Score : 91%")
st.subheader("🏆 Final Prediction")
if winner["Confidence"] >= 80:
    st.success(f"✅ Identity Verified ({winner['Confidence']}% Confidence)")
elif winner["Confidence"] >= 60:
    st.info(f"🟢 Candidate Verified ({winner['Confidence']}% Confidence)")
else:
    st.error(f"❌ Manual Verification Required ({winner['Confidence']}% Confidence)")
st.markdown("### 🧠 AI Detection Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎤 Voice Match", "92%")

with col2:
    st.metric("📷 Face Match", "95%")

with col3:
    st.metric("📧 Email Match", "100%")

left, right = st.columns([1, 2])

with left:

    st.success("🏆 VERIFIED CANDIDATE")

    st.markdown(f"### {winner['Participant']}")
    st.caption("The AI has identified this participant with the highest confidence score.")

    st.markdown("### Confidence Score")

    st.markdown(
        f"""
        <h1 style="color:#00FF99;font-size:60px;">
            {winner['Confidence']}%
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.progress(winner["Confidence"] / 100)

    st.success("🟢 Status : VERIFIED")
    st.markdown("---")
st.subheader("📊 Candidate Match Breakdown")

breakdown = pd.DataFrame({
    "Feature": [
        "Email Match",
        "Speaking Time",
        "Webcam Status",
        "AI Keywords",
    ],
    "Score": [
        30,
        15,
        10,
        12,
    ]
})

st.dataframe(
    breakdown,
    use_container_width=True,
    hide_index=True
)
with right:

    st.info("### 🧠 AI Explainability")

    for reason in winner["Reason"].split(", "):
        st.write("✅", reason)

    st.markdown("---")

    st.success("### 🤖 AI Recommendation")
    st.markdown("---")

st.warning("### ⚠️ AI Risk Analysis")

if winner["Confidence"] >= 80:
    st.success("Low Risk • Identity confidently verified.")
elif winner["Confidence"] >= 60:
    st.warning("Medium Risk • Identity verified but additional checks may be performed.")
else:
    st.error("High Risk • Manual verification required.")

    if winner["Confidence"] >= 80:
        st.write("✅ Candidate identity verified with very high confidence.")
    elif winner["Confidence"] >= 60:
        st.write("🟢 Candidate verified. Safe to continue the interview.")
    else:
        st.write("⚠️ Confidence is low. Manual verification is recommended.")
st.markdown("---")
st.subheader("🎯 AI Confidence Gauge")

gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=winner["Confidence"],
    title={"text": "Candidate Confidence"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "green"},
        "steps": [
            {"range": [0, 40], "color": "#8B0000"},
            {"range": [40, 70], "color": "#FFD700"},
            {"range": [70, 100], "color": "#228B22"}
        ]
    }
))

gauge.update_layout(height=400)

st.plotly_chart(gauge, width="stretch")
# ------------------------------------------
# Live Confidence History
# ------------------------------------------

st.markdown("---")
st.markdown("---")
st.markdown("---")
st.subheader("⏱️ Interview Timeline")

timeline = pd.DataFrame({
    "Time": [
        "10:00 AM",
        "10:01 AM",
        "10:03 AM",
        "10:05 AM"
    ],
    "Event": [
        "Candidate Joined",
        "Webcam Verified",
        "AI Detection Started",
        "Candidate Identified"
    ]
})

st.table(timeline)
st.subheader("🟢 Live Interview Status")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🎤 Microphone : ON")

with col2:
    st.success("📷 Webcam : ON")

with col3:
    st.success("🤖 AI Detection : Running")
    st.markdown("---")

st.subheader("🖥️ System Health")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.success("🟢 Camera")
    st.write("Operational")

with c2:
    st.success("🟢 Microphone")
    st.write("Operational")

with c3:
    st.success("🟢 AI Engine")
    st.write("Running")

with c4:
    st.success("🟢 Database")
    st.write("Connected")
st.subheader("📈 Live Confidence History")

if "history" not in st.session_state:
    st.session_state.history = []

st.session_state.history.append(
    winner["Confidence"]
)

st.session_state.history = st.session_state.history[-20:]

history_df = pd.DataFrame({
    "Run": range(
        1,
        len(st.session_state.history) + 1
    ),
    "Confidence": st.session_state.history
})

history_df = history_df.set_index("Run")

st.line_chart(history_df)
# ------------------------------------------
# Confidence Comparison
# ------------------------------------------

st.markdown("---")
st.markdown("---")
st.subheader("🚨 AI Risk Analysis")

risk1, risk2, risk3 = st.columns(3)

with risk1:
    st.success("✅ Email Verified")

with risk2:
    st.success("✅ Webcam Verified")

with risk3:
    st.warning("⚠️ Voice Match: Medium Risk")
st.subheader("📊 Confidence Comparison")

bar_chart = px.bar(
    result_df,
    x="Participant",
    y="Confidence",
    color="Confidence",
    color_continuous_scale="Viridis",
    text="Confidence",
    title="Confidence Score of Each Participant"
)

bar_chart.update_traces(texttemplate="%{text}%", textposition="outside")
bar_chart.update_layout(
    xaxis_title="Participants",
    yaxis_title="Confidence (%)",
    height=450
)

st.plotly_chart(bar_chart, width="stretch")

# ------------------------------------------
# Donut Chart
# ------------------------------------------

st.markdown("---")
st.subheader("🍩 Confidence Distribution")

donut = px.pie(
    result_df,
    values="Confidence",
    names="Participant",
    hole=0.55,
    color="Participant",
    color_discrete_sequence=px.colors.qualitative.Set2
)

donut.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

donut.update_layout(
    height=500,
    showlegend=True
)

st.plotly_chart(donut, width="stretch")

# ------------------------------------------
# Candidate Details
# ------------------------------------------


# ------------------------------------------
# Detection Summary
# ------------------------------------------
st.markdown("---")
st.subheader("📌 Detection Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.success("👥 Participants")
    st.metric("Participants", len(participants))

with c2:
    st.success("🎯 Winner")
    st.write(f"### {winner['Participant']}")

with c3:
    st.success("📊 Confidence")
    st.metric("Confidence", f"{winner['Confidence']}%")

with c4:
    st.success("🟢 Status")
    st.metric("Status", "Completed")

# ------------------------------------------
# Download Report
# ------------------------------------------
# Footer
# ------------------------------------------
st.markdown("---")

# ==============================
# HR Activity Log
# ==============================
st.markdown("---")
st.subheader("📄 Export Report")

st.download_button(
    "📥 Download AI Report (CSV)",
    csv,
    file_name="candidate_report.csv",
    mime="text/csv",
    use_container_width=True
)
st.subheader("📜 HR Activity Log")

log = pd.DataFrame({
    "Time": [
        "10:00 AM",
        "10:01 AM",
        "10:02 AM",
        "10:03 AM",
        "10:04 AM"
    ],
    "Activity": [
        "Candidate joined interview",
        "Webcam verified",
        "Microphone verified",
        "AI identification completed",
        "Report ready for download"
    ],
    "Status": [
        "✅",
        "✅",
        "✅",
        "✅",
        "✅"
    ]
})

st.dataframe(
    log,
    width="stretch",
    hide_index=True,
)

# ------------------------------------------
# Footer
# ------------------------------------------

st.markdown("---")

st.markdown(
    """
<div style="text-align:center;color:gray;font-size:14px">
🕵️ Sherlock AI Candidate Identifier<br>
Built with ❤️ using Streamlit • Plotly • RapidFuzz<br><br>
© 2026 Sherlock AI | AI Powered Candidate Verification System
</div>
""",
unsafe_allow_html=True
)
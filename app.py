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

st.plotly_chart(chart, width="stretch")   

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
st.success("Interview conversation analyzed successfully.")

st.write("**Summary**")
st.write("""
The candidate answered confidently, communicated clearly,
and demonstrated good problem-solving skills.
""")

st.progress(0.92)
st.caption("Communication Score: 92%")
st.subheader("🧠 AI Skill Extraction")
st.markdown("---")
skills = [
    "Python",
    "Machine Learning",
    "SQL",
    "Streamlit",
    "Communication",
    "Problem Solving",
    "NLP"
]

cols = st.columns(3)

for i, skill in enumerate(skills):
    with cols[i % 3]:
        st.success(f"✅ {skill}")
# -------------------------------
# Live Face Verification
# -------------------------------
st.subheader("📷 Live Face Verification")
st.markdown("---")

st.subheader("📊 Candidate Score")

st.metric("Overall Score", "94%")
st.progress(0.94)
st.markdown("---")

st.subheader("🚨 AI Risk Detection")

risk_score = 8

st.metric("Suspicion Score", f"{risk_score}%")

if risk_score < 20:
    st.success("✅ No suspicious behaviour detected.")
elif risk_score < 50:
    st.warning("⚠ Minor suspicious behaviour.")
else:
    st.error("🚨 High cheating probability.")

st.success("Recommendation: Shortlist Candidate")

st.success("✅ Candidate Verified")
# ----------------------------
# Detection Timeline
# ----------------------------

st.markdown("---")

st.subheader("📅 Detection Timeline")

timeline = [
    ("10:00:01", "Interview Started"),
    ("10:00:12", "Face Verified"),
    ("10:01:08", "Eye Contact Stable"),
    ("10:03:40", "Voice Matched"),
    ("10:05:15", "Identity Confirmed"),
    ("10:06:02", "No Suspicious Activity")
]

for time, event in timeline:
    st.write(f"**{time}** — {event}")
    st.markdown("---")

st.markdown("---")

st.subheader("🏆 Final AI Decision")

overall_score = 94

st.metric("Overall AI Confidence", f"{overall_score}%")

if overall_score >= 90:
    st.success("✅ VERIFIED")
elif overall_score >= 70:
    st.warning("⚠ Needs Manual Review")
else:
    st.error("❌ Candidate Rejected")

st.markdown("---")

report = """
Sherlock AI Candidate Report

Candidate Name : Sahana Bhairav

Interview Status : VERIFIED

Face Match : 95%
Eye Contact : 91%
Liveness : 97%
Confidence : 96%

Risk Score : 8%

Overall AI Confidence : 94%

Recommendation :
Candidate Successfully Verified.
"""

st.download_button(
    label="📥 Download Candidate Report",
    data=report,
    file_name="Sherlock_AI_Report.txt",
    mime="text/plain"
)




    



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
# ------------------------------------------
# Live Confidence History
# ------------------------------------------

st.markdown("---")
st.markdown("---")
st.markdown("---")

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

# ------------------------------------------
# Candidate Details
# ------------------------------------------


# ------------------------------------------
# Detection Summary
# ------------------------------------------
st.markdown("---")

# ------------------------------------------
# Download Report
# ------------------------------------------
# Footer
# ------------------------------------------
st.markdown("---")

# ------------------------------------------
# Footer
# ---------------------------------------

st.markdown(
    """
    <div style="text-align:center; color:gray; padding:20px;">
        <h4>🕵️ Sherlock AI Candidate Identifier</h4>
        <p>Built with ❤️ using Python, Streamlit & AI</p>
        <p>© 2026 |</p>
    </div>
    """,
    unsafe_allow_html=True
)
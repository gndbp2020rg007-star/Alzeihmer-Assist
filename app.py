
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import tempfile

st.set_page_config(page_title="Alzheimer Assist", layout="centered")

# ---------------- Utility ----------------
def stage_from_scores(mmse, moca):
    if mmse >= 24 and moca >= 26:
        return "Normal cognition"
    if mmse >= 21 or moca >= 18:
        return "MCI (Mild Cognitive Impairment)"
    if mmse >= 10:
        return "Mild–Moderate Alzheimer-consistent pattern"
    return "Severe Alzheimer-consistent pattern"

# ---------------- Mode Selection ----------------
mode = st.sidebar.selectbox("Select Mode", ["Patient / Family", "Doctor"])

st.title("Alzheimer Assist – Clinical Decision Support Tool")
st.warning("Assistive tool only. Final diagnosis must be made by a qualified physician.")

# ---------------- Patient Details ----------------
st.header("Patient Details (Mandatory)")
name = st.text_input("Patient Name")
age = st.number_input("Age", 1, 120)
sex = st.selectbox("Sex", ["Male", "Female", "Other"])

if not name:
    st.stop()

# ---------------- WHO-Aligned History ----------------
with st.expander("WHO-aligned Medical & Lifestyle History (Optional)"):
    diabetes = st.checkbox("Diabetes")
    hypertension = st.checkbox("Hypertension")
    stroke = st.checkbox("History of stroke")
    depression = st.checkbox("Depression")
    family = st.checkbox("Family history of dementia")
    smoking = st.selectbox("Smoking status", ["Unknown","Never","Former","Current"])
    alcohol = st.selectbox("Alcohol use", ["Unknown","None","Moderate","High"])
    activity = st.selectbox("Physical activity", ["Low","Moderate","High"])

# ---------------- MMSE ----------------
st.header("MMSE Screening")
mmse_questions = [
    ("What is the year?", 1),
    ("What is the month?", 1),
    ("Where are you right now?", 1),
    ("Spell WORLD backwards", 1),
    ("Recall the word APPLE", 1)
]
mmse_score = 0
for q, pts in mmse_questions:
    if st.radio(q, ["Correct","Incorrect"], key=q) == "Correct":
        mmse_score += pts

# ---------------- MoCA ----------------
st.header("MoCA Screening")
moca_questions = [
    ("Draw a clock correctly", 1),
    ("Name the animal shown", 1),
    ("Recall 5 words", 5),
    ("Serial subtraction", 3)
]
moca_score = 0
for q, pts in moca_questions:
    if st.radio(q, ["Correct","Incorrect"], key="m"+q) == "Correct":
        moca_score += pts

# ---------------- Results ----------------
if st.button("Generate Cognitive Results"):
    stage = stage_from_scores(mmse_score, moca_score)

    st.subheader("Scores & Severity Staging")
    st.metric("MMSE Score", mmse_score)
    st.metric("MoCA Score", moca_score)
    st.success(f"Severity staging: {stage}")

    # Graphical bands
    fig, ax = plt.subplots()
    ax.bar(["MMSE","MoCA"], [mmse_score, moca_score])
    ax.axhline(24, linestyle="--", label="MMSE cutoff")
    ax.axhline(26, linestyle="--", label="MoCA cutoff")
    ax.legend()
    st.pyplot(fig)

    # ---------------- PDF Report ----------------
    if st.button("Download PDF Report"):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        doc = SimpleDocTemplate(tmp.name)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("Alzheimer Assist – Screening Report", styles["Title"]),
            Spacer(1,12),
            Paragraph(f"Patient: {name}, Age: {age}, Sex: {sex}", styles["Normal"]),
            Spacer(1,12),
            Paragraph(f"MMSE Score: {mmse_score}", styles["Normal"]),
            Paragraph(f"MoCA Score: {moca_score}", styles["Normal"]),
            Spacer(1,12),
            Paragraph(f"Severity staging: {stage}", styles["Normal"]),
            Spacer(1,12),
            Paragraph("This report is assistive only and must be interpreted by a clinician.", styles["Italic"])
        ]
        doc.build(story)
        with open(tmp.name,"rb") as f:
            st.download_button("Download PDF", f, file_name="Alzheimer_Assist_Report.pdf")

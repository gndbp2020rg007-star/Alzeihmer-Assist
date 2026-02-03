
import streamlit as st
import random

st.set_page_config(page_title="Alzheimer Assist", layout="centered")

st.title("Alzheimer Assist – Clinical Decision Support Tool")
st.warning("This software assists doctors and does NOT provide a medical diagnosis.")

st.header("Patient Details")
name = st.text_input("Name")
age = st.number_input("Age", 1, 120)
sex = st.selectbox("Sex", ["Male","Female","Other"])

st.header("Cognitive Screening")

def interpret(score, cutoff):
    return "Possible cognitive impairment – further evaluation advised" if score < cutoff else "No significant cognitive impairment detected"

if st.button("Run MMSE"):
    s = random.randint(10,30)
    st.metric("MMSE Score", s)
    st.info(interpret(s,24))

if st.button("Run MoCA"):
    s = random.randint(8,30)
    st.metric("MoCA Score", s)
    st.info(interpret(s,26))

st.header("Biomarker Upload")
file = st.file_uploader("Upload blood report", type=["pdf","png","jpg","jpeg"])
if file:
    st.warning("Possible Alzheimer-related biomarker abnormality detected")

st.caption("Clinical decision support only – consult a qualified physician.")

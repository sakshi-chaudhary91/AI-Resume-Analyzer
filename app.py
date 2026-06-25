import streamlit as st
import pdfplumber
from skill_extractor import extract_skills
from ats_score import calculate_ats_score
from skill_gap import find_missing_skills

st.title("AI Resume Analyser")
uploaded_file = st.file_uploader(
    "Upload Resume",
    type = ["pdf"]
)
if uploaded_file:
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:
            page_text = page.extract_text()
            text += page_text + "\n"

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        text,
        height = 300
    )
    skills = extract_skills(text)
    missing_skills = find_missing_skills(skills)
    ats_result = calculate_ats_score(text, skills)
    st.subheader("Detected Skills")

    if skills:
     for skill in skills:
        st.write(f"✅ {skill}")

    else:
       st.warning("No skills detected.")

    st.subheader("Missing Skills")
    if missing_skills:
      for skill in missing_skills:
        st.write(f"❌ {skill}")
    else:
        st.success("No Missing Skills Found")

    st.subheader("ATS Score")
    st.success(f"Overall ATS Score: {ats_result['Total']}/100")
    st.write("### Score Breakdown")
    st.write(f"Skills: {ats_result['Skills']}/40")
    st.write(f"Projects: {ats_result['Projects']}/20")
    st.write(f"Education: {ats_result['Education']}/10")
    st.write(f"Contact: {ats_result['Contact']}/20")
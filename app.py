import streamlit as st
import pandas as pd
import plotly.express as px
import pdfplumber
from skill_extractor import extract_skills
from ats_score import calculate_ats_score
from skill_gap import find_missing_skills
from ai_engine import get_ai_suggestions
from role_skills import find_role_missing_skills

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

div[data-testid="metric-container"] {
    background-color: #f5f7fa;
    border: 1px solid #e6e6e6;
    padding: 15px;
    border-radius: 12px;
}

.stButton button {
    width: 100%;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("🚀 AI Resume Analyzer")
st.caption(
    "ATS Scoring  • Skill Gap Analysis  • AI Recommendations  • Career Insights"
)

# Layout split (UI improvement only)
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF only)",
        type=["pdf"]
    )

with col2:
    st.info("📌 Get ATS Score, Missing Skills & Resume Analysis instantly")

if uploaded_file:
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            text += page_text + "\n"

    st.divider()

    # ===== Extracted Text =====
    st.subheader("📄 Extracted Resume Text")
    st.text_area("Resume Content", text, height=250)

    # ==== Target Role =====
    selected_role = st.selectbox(
       "Target Role",
       [
          "AI Engineer",
          "Data Analyst",
          "Frontend Developer"
       ]
    )

    # ===== Processing =====
    skills = extract_skills(text)
    missing_skills = find_missing_skills(skills)
    ats_result = calculate_ats_score(text, skills)
    role_missing = find_role_missing_skills(
       selected_role,
       skills
    )
    score = ats_result["Total"]
    if score >= 90:
      strength = "🚀 Expert"
    elif score >= 75:
      strength = "💪 Strong"
    elif score >= 60:
      strength = "📈 Intermediate"
    else:
      strength = "🌱 Beginner"

    st.divider()

    # ===== ATS DASHBOARD =====

    st.subheader("📊 ATS Dashboard")
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    with col_stats1:
     st.metric(
        "ATS Score",
        f"{ats_result['Total']}/100"
    )

    with col_stats2:
     st.metric(
        "Skills Found",
        len(skills)
    )

    with col_stats3:
     st.metric(
        "Missing Skills",
        len(missing_skills)
    )
     
     with col_stats4:
        st.metric(
           "Level",
           strength
        )

    st.progress(ats_result["Total"] / 100)

    st.write("### Score Breakdown")

    col3, col4, col5, col6 = st.columns(4)

    with col3:
     st.metric("Skills", f"{ats_result['Skills']}/40")

    with col4:
     st.metric("Projects", f"{ats_result['Projects']}/20")

    with col5:
     st.metric("Education", f"{ats_result['Education']}/10")

    with col6:
     st.metric("Contact", f"{ats_result['Contact']}/20")

    st.divider()

    # ===== SKILLS =====
    st.subheader("🧠 Detected Skills")
    if skills:
      col_a, col_b = st.columns(2)
      with col_a:
        for skill in skills:
            st.success(f"✅ {skill}")

      with col_b:
        skill_counts = []
        for skill in skills:
           count = text.lower().count(skill.lower())
           skill_counts.append(count)

        df = pd.DataFrame({
            "Skills": skills,
            "Count": skill_counts
        })

        fig_bar = px.bar(
            df,
            x="Skills",
            y="Count",
            title="Skill Frequency"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )
        fig_pie = px.pie(
           df,
           names = "Skills",
           values = "Count",
           title = "Skill Distribution"
        )
        st.plotly_chart(
           fig_pie,
           use_container_width = True
        )
    else:
        st.warning("No skills detected.")

    st.subheader("Resume Level")
    if score >= 90:
      st.success("🚀 Excellent Resume")
    elif score >= 75:
      st.success("💪 Strong Resume")
    elif score >= 60:
      st.warning("📈 Improving Resume")
    else:
      st.error("🌱 Needs Improvement")

    # ==== Missing skill ====

    st.subheader("❌ Missing Skills")

    if missing_skills:
        for skill in missing_skills:
            st.error(f"❌ {skill}")
    else:
        st.success("No Missing Skills Found 🎉")

     # ==== Role based missing skill====
    st.subheader(
       f"Missing skill for {selected_role}"
    ) 
    if role_missing:
       for skill in role_missing:
          st.error(f" ❌{skill}")
    else:
       st.success("You match this role very well!")  

    # ==== AI Suggestion =====

    st.subheader("🤖 AI Suggestions")
    ai_result = ""
    if st.button("Get AI Suggestions"):
      with st.spinner("Analyzing with AI..."):
        ai_result = get_ai_suggestions(text)
      st.success("Analysis Complete ✅")
      st.markdown(ai_result)

    # ==== Report Text ====

    report_text = f"""
    AI RESUME ANALYSIS REPORT

=================================

    ATS Score: {ats_result['Total']}/100
    Detected Skills:
    {', '.join(skills)}
    Missing Skills:
    {', '.join(missing_skills)}
    Role-Based Missing Skills:
    {', '.join(role_missing)}

=================================

    AI Suggestions:
    {ai_result if ai_result else 'Generate AI Suggestions first.'}
     """

   # ==== Download Resume ====
    st.subheader("Download Analysis Resume")
    st.download_button(
       label="📥 Download Report",
       data=report_text,
    file_name="resume_analysis_report.txt",
      mime="text/plain"
    )
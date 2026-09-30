import os
import re
import time

import streamlit as st

# Load the API key from Streamlit Secrets (or an existing environment variable)
try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

from crew import run_admission_crew
from data import BACKGROUNDS, DISCLAIMER, PROGRAMS

st.set_page_config(page_title="CUI Admission Assistant", page_icon="🎓", layout="wide")

st.title("🎓 COMSATS University Islamabad – Admission Assistant")
st.caption("Multi-agent AI system (CrewAI + Groq). Sample data – always verify with official CUI admission information.")

SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
            "Statistics", "Economics", "Accounting/Business", "English", "Other"]

with st.form("student_form"):
    st.subheader("Student Profile")
    name = st.text_input("Student name (optional)")

    c1, c2 = st.columns(2)
    with c1:
        qualification = st.selectbox("Academic qualification status", [
            "Intermediate (FSc/FA/ICS/I.Com) completed",
            "A-Level completed",
            "Intermediate/A-Level appearing (result awaited)",
            "DAE (Diploma) completed",
        ])
        matric_system = st.selectbox("Matric / O-Level", ["Matric", "O-Level"])
        matric_pct = st.number_input("Matric/O-Level percentage", 0.0, 100.0, 70.0, 0.5)
    with c2:
        background = st.selectbox("Intermediate/A-Level group", BACKGROUNDS)
        inter_pct = st.number_input("Intermediate/A-Level percentage (or expected)", 0.0, 100.0, 70.0, 0.5)
        cgpa = st.text_input("CGPA (if applicable, e.g. DAE/A-Level equivalence)")

    subjects = st.multiselect("Subjects studied", SUBJECTS, default=["Mathematics", "Physics"])

    c3, c4 = st.columns(2)
    with c3:
        test_taken = st.selectbox("Entry test", ["Not taken yet", "CUI/NTS entry test", "SAT", "Other"])
    with c4:
        test_score = st.number_input("Entry test score (%) – if taken", 0.0, 100.0, 0.0, 0.5)

    preferred = st.selectbox("Preferred program", ["Not sure – suggest for me"] + [p["name"] for p in PROGRAMS])
    interests = st.text_area("Skills / interests", placeholder="e.g. programming, problem solving, design, business...")
    extra = st.text_area("Other relevant information (optional)")

    submitted = st.form_submit_button("Analyze my admission chances", type="primary")

if submitted:
    profile = {
        "name": name or "Student",
        "qualification": qualification,
        "matric_system": matric_system,
        "matric_pct": matric_pct,
        "background": background,
        "inter_pct": inter_pct,
        "cgpa": cgpa or "N/A",
        "subjects": ", ".join(subjects) or "Not provided",
        "entry_test": test_taken if test_taken == "Not taken yet" else f"{test_taken}: {test_score}%",
        "preferred": None if preferred.startswith("Not sure") else preferred,
        "interests": interests or "Not provided",
        "extra": extra or "None",
    }
    try:
        start = time.time()
        with st.spinner("Agents are working in parallel..."):
            res = run_admission_crew(profile)
        st.success(f"Analysis complete in {time.time() - start:.1f}s")

        # Parse status line from the eligibility output
        elig = res["eligibility"]
        m = re.search(r"STATUS:\s*(.+)", elig, re.IGNORECASE)
        status = m.group(1).strip() if m else "See details"
        elig_body = re.sub(r"STATUS:\s*.+\n?", "", elig, count=1, flags=re.IGNORECASE)

        tabs = st.tabs(["📋 Requirements", "✅ Eligibility", "🎯 Recommendations", "📝 Final Summary"])
        with tabs[0]:
            st.markdown(res["requirements"])
        with tabs[1]:
            low = status.lower()
            if "not met" in low:
                st.error(f"Status: {status}")
            elif "potential" in low:
                st.warning(f"Status: {status}")
            elif "eligible" in low:
                st.success(f"Status: {status}")
            else:
                st.info(f"Status: {status}")
            st.markdown(elig_body)
        with tabs[2]:
            st.markdown(res["recommendation"])
        with tabs[3]:
            st.markdown(res["summary"])
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.info("Check that GROQ_API_KEY is set in Streamlit Secrets. If you see a rate-limit (429) error, wait a minute and try again.")

st.divider()
st.caption(DISCLAIMER)

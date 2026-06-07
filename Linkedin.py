import streamlit as st

st.title("LinkedIn Profile Analyzer")

name = st.text_input("Enter Your Name")
skills = st.text_area("Enter Your Skills (comma separated)")

if st.button("Analyze Profile"):

    skill_list = [s.strip() for s in skills.split(",")]

    score = min(len(skill_list) * 10, 100)

    st.subheader("Profile Analysis")
    st.write(f"Profile Score: {score}/100")

    if score < 50:
        st.warning("Add more technical skills and projects.")
    else:
        st.success("Good profile!")

    st.subheader("Recommended Skills")
    recommendations = [
        "Python",
        "SQL",
        "GitHub",
        "Machine Learning",
        "Prompt Engineering"
    ]

    for skill in recommendations:
        if skill not in skill_list:
            st.write(f"✅ {skill}")

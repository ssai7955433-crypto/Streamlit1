import streamlit as st

st.title("AI Learning Path Generator")

skill = st.text_input("Enter Skill")

if st.button("Generate"):
    roadmap = f"""
    Beginner:
    - Basics of {skill}
    - Variables and Functions

    Intermediate:
    - Projects in {skill}
    - APIs and Frameworks

    Advanced:
    - Real-world Applications
    - Deployment

    Timeline:
    0-2 Months : Beginner
    2-4 Months : Intermediate
    4-6 Months : Advanced
    """
    st.write(roadmap)

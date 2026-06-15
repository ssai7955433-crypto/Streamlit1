import streamlit as st
import base64

if st.button("Generate Birthday Wish"):

    st.balloons()

    st.image("su.jpeg", use_container_width=True)

    with open("suh.mpeg", "rb") as f:
        audio_bytes = f.read()

    audio_base64 = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg">
    </audio>
    """

    st.markdown(audio_html, unsafe_allow_html=True)

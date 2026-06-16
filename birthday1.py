import streamlit as st
import base64

FRIEND_NAME = "Suhitha"

st.set_page_config(page_title="Happy Birthday", page_icon="🎂")

st.title("🎉 Birthday Surprise 🎉")

if st.button("Generate Birthday Wish"):

    st.balloons()

    st.markdown(f"""
# 🎂 Happy Birthday {FRIEND_NAME}! 🎂

Wishing you a wonderful day filled with happiness,
success, laughter, and countless beautiful memories! 🎉🎈🎁
Your kindness,
support, and friendship make every moment special.
I am truly grateful to have a friend like you in my life.
May this year bring you endless opportunities, good health,
great achievements, and all the happiness you deserve.
May all your dreams come true and may your smile always shine brightly.
No matter where life takes us, our friendship will always remain strong.
Thank you for standing by me through good times and bad.
Thank you for being such an amazing friend.
Once again Happy Birthday Attitude Pilla 😆❤️‍🩹💗!."PARTY Mukhyam Mey".

💖 Friends Forever! 💖
""")

    # Show two images
    col1, col2 = st.columns(2)

    with col1:
        st.image("suhi.jpeg", caption="Aunty 😁", use_container_width=True)

    with col2:
        st.image("att.jpeg", use_container_width=True)

    # Auto-play song
    with open("attit.mpeg", "rb") as f:
        audio_bytes = f.read()

    audio_base64 = base64.b64encode(audio_bytes).decode()

    st.markdown(
        f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True,
    )

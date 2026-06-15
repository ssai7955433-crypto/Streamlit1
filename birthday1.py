import streamlit as st

FRIEND_NAME = "Suhitha"
PHOTO_PATH = "su.jpeg"

st.title("🎉 Birthday Surprise 🎉")

if st.button("Generate Birthday Wish"):

    st.balloons()

    st.markdown(f"""
    # 🎂 Happy Birthday {FRIEND_NAME}! 🎂

    Wishing you a wonderful day filled with happiness,
    success, laughter, and countless beautiful memories! 🎉🎈🎁
    Thank you for being such an amazing friend.Your kindness, support, andfriendship
make every moment special.I am truly grateful to have a friendlike you in my life.May this year bring
you endless opportunities, goodhealth, great achievements, andall the happiness you deserve.May all
your dreams come true andmay your smile always shine brightly.No matter where life takes us, our
friendship will always remain strong.Thank you for standing by me through goodtimes andbad.
Friends like you are rare andprecious.Wishing you a birthday filledwith love, joy, fun, andunforgettable
moments.Enjoy your special day to the fullest!🎂Happy BirthdayOnce Again, Attitude pilla😆❤️‍🩹💗!

    ❤️ Friends Forever! ❤️
    """)

    # Show photo only after button click
    st.image(PHOTO_PATH, use_container_width=True)

    # Play song only after button click
    audio_file = open("suh.mpeg", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mpeg")

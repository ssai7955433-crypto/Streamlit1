import streamlit as st
from PIL import Image

# Set your friend's details here
FRIEND_NAME = "Suhitha"
PHOTO_PATH = "su.jpeg"   # Keep photo in same folder

st.set_page_config(page_title="Happy Birthday", page_icon="🎂")

st.title("🎉 Birthday Surprise 🎉")

if st.button("Generate Birthday Wish"):
   st.balloons()
   st.markdown(
    f"""
    # 🎂 Happy Birthday {FRIEND_NAME}! 🎂

    Wishing you a wonderful day filled with happiness,
    success, laughter, and countless beautiful memories! 🎉🎈🎁

    Thank you for being such an amazing friend. Your kindness,
    support, and friendship make every moment special. I am truly
    grateful to have a friend like you in my life.

    May this year bring you endless opportunities, good health,
    great achievements, and all the happiness you deserve. May all
    your dreams come true and may your smile always shine brightly.

    No matter where life takes us, our friendship will always remain
    strong. Thank you for standing by me through good times and bad.
    Friends like you are rare and precious.

    Wishing you a birthday filled with love, joy, fun, and unforgettable
    moments. Enjoy your special day to the fullest!

    🎂 Happy Birthday Once Again, {FRIEND_NAME}! 🎂

    💖 Friends Forever! 💖
    """
)
image = Image.open(PHOTO_PATH)
st.image(image, caption=f"Happy Birthday {FRIEND_NAME}", use_container_width=True)

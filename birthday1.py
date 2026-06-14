import streamlit as st

FRIEND_NAME = "Suhitha"
PHOTO_PATH = "su.jpeg"  # or your image URL

st.set_page_config(page_title="Happy Birthday", page_icon="🎂")

st.title("🎉 Birthday Surprise 🎉")

show_wish = st.button("Generate Birthday Wish")

if show_wish:
    st.balloons()

    st.markdown(f"""
# 🎂 Happy Birthday {FRIEND_NAME}! 🎂

Wishing you a wonderful day filled with happiness,
success, laughter, and countless beautiful memories! 🎉🎈🎁

Thank you for being such an amazing friend.

❤️ Friends Forever! ❤️
""")

    st.image(
        PHOTO_PATH,
        caption=f"Happy Birthday {FRIEND_NAME}",
        use_container_width=True
    )

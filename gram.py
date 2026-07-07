import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Grammar Checker", page_icon="📝")

st.title("📝 AI Grammar Checker")
st.write("Correct grammar, improve writing, rewrite professionally, and explain grammar mistakes.")

text = st.text_area("Enter your sentence:", height=150)

if st.button("Check Grammar"):

    if text.strip() == "":
        st.warning("Please enter some text.")
    else:

        prompt = f"""
You are an English Grammar Expert.

Analyze the following sentence.

Sentence:
{text}

Return the response in this format:

### Corrected Sentence
...

### Improved Writing
...

### Professional Rewrite
...

### Grammar Mistakes
- Explain each grammar mistake in simple English.
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response.choices[0].message.content

            st.success("Analysis Complete")
            st.markdown(result)

        except Exception as e:
            st.error(f"Error: {e}")

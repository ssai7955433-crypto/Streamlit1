"""
ai_writing_assistant.py
========================
ContentCo — AI Writing Assistant

A full-stack Streamlit app demonstrating a real-world internal AI tool:
one app for a content team to generate blogs, emails, social posts,
ad copy, and translations — with brand tone, content history, and
one-click downloads.

Run with:
    streamlit run ai_writing_assistant.py

Requires a .env file (copy from .env.example) with:
    GROQ_API_KEY=...
    GOOGLE_API_KEY=...
"""

import streamlit as st
from datetime import datetime

from utils.ai_client import generate, translate, keys_configured
from utils.prompts import (
    BLOG_SYSTEM, BLOG_USER,
    EMAIL_SYSTEM, EMAIL_USER,
    SOCIAL_SYSTEM, SOCIAL_USER, PLATFORM_RULES,
    AD_SYSTEM, AD_USER,
    TRANSLATION_LANGUAGES,
)

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ContentCo — AI Writing Assistant",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ──────────────────────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []          # list of dicts: type, content, time, meta
if "last_output" not in st.session_state:
    st.session_state.last_output = ""       # used by Translator tab "translate last output"


def save_to_history(content: str, content_type: str, meta: str = ""):
    """Store generated content in session history and remember as 'last output'."""
    st.session_state.last_output = content
    st.session_state.history.append({
        "type": content_type,
        "content": content,
        "time": datetime.now().strftime("%H:%M:%S"),
        "meta": meta,
    })


def render_result(content: str, content_type: str, filename_prefix: str):
    """Common UI block: success message, content display, download buttons."""
    st.success(f"✅ {content_type} generated!")
    st.markdown(content)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Download as .txt",
            content,
            file_name=f"{filename_prefix}_{timestamp}.txt",
            mime="text/plain",
            use_container_width=True,
            key=f"dl_txt_{filename_prefix}_{timestamp}",
        )
    with col2:
        st.download_button(
            "📥 Download as .md",
            content,
            file_name=f"{filename_prefix}_{timestamp}.md",
            mime="text/markdown",
            use_container_width=True,
            key=f"dl_md_{filename_prefix}_{timestamp}",
        )


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Brand settings + API key check + history controls
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("✍️ ContentCo")
    st.caption("AI Writing Assistant — Internal Tool")
    st.divider()

    # API key status
    keys = keys_configured()
    if not keys["groq"] or not keys["gemini"]:
        st.warning("⚠️ API keys missing")
        if not keys["groq"]:
            st.caption("Missing **GROQ_API_KEY** — generation tabs won't work")
        if not keys["gemini"]:
            st.caption("Missing **GOOGLE_API_KEY** — translator won't work")
        with st.expander("How to fix"):
            st.markdown(
                "1. Copy `.env.example` to `.env`\n"
                "2. Get a free Groq key: https://console.groq.com\n"
                "3. Get a free Gemini key: https://aistudio.google.com/app/apikey\n"
                "4. Paste both keys into `.env`\n"
                "5. Restart the app"
            )
    else:
        st.success("✅ API keys loaded")

    st.divider()

    # Brand settings — used across all tabs
    st.subheader("Brand Settings")
    brand = st.text_input("Brand / Company Name", value="ContentCo")
    tone = st.selectbox(
        "Default Brand Tone",
        ["Professional", "Casual", "Formal", "Friendly", "Persuasive", "Witty"],
    )
    temperature = st.slider(
        "Creativity (temperature)", 0.0, 1.5, 0.7, 0.1,
        help="0 = focused & predictable, 1.5 = highly creative & varied",
    )

    st.divider()

    # Session stats + history controls
    st.metric("Items generated this session", len(st.session_state.history))
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.session_state.last_output = ""
        st.rerun()

    if st.session_state.history:
        bulk_text = ("\n\n" + ("=" * 60) + "\n\n").join(
            f"[{item['time']}] {item['type']}"
            + (f" — {item['meta']}" if item["meta"] else "")
            + f"\n\n{item['content']}"
            for item in st.session_state.history
        )
        st.download_button(
            "📦 Download All (bulk)",
            bulk_text,
            file_name=f"contentco_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ──────────────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────────────
st.title(f"✍️ AI Writing Assistant — {brand}")
st.caption(
    f"Brand tone: **{tone}**  |  Powered by Groq (generation) + Gemini (translation)"
)

tab_blog, tab_email, tab_social, tab_ad, tab_translate, tab_about = st.tabs(
    ["📝 Blog Post", "📧 Email", "📱 Social Media", "📣 Ad Copy", "🌐 Translate", "ℹ️ About"]
)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — BLOG POST GENERATOR
# ──────────────────────────────────────────────────────────────────────────────
with tab_blog:
    st.subheader("📝 Blog Post Generator")
    st.caption("Generate SEO-friendly blog posts tailored to your audience.")

    c1, c2, c3 = st.columns(3)
    with c1:
        blog_topic = st.text_input(
            "Blog Topic", placeholder="e.g. 5 AI Tools Every Marketer Should Know",
            key="blog_topic",
        )
    with c2:
        blog_audience = st.selectbox(
            "Target Audience",
            ["General Public", "Students", "Professionals", "Executives", "Small Business Owners"],
            key="blog_audience",
        )
    with c3:
        blog_length = st.select_slider(
            "Length (words)", [300, 500, 800, 1200, 1500], value=500, key="blog_length",
        )

    c4, c5 = st.columns(2)
    with c4:
        blog_keywords = st.text_input(
            "SEO Keywords (comma-separated)",
            placeholder="AI, marketing automation, productivity",
            key="blog_keywords",
        )
    with c5:
        blog_sections = st.slider("Number of Sections", 2, 8, 4, key="blog_sections")

    if st.button("Generate Blog Post", type="primary", key="blog_btn"):
        if not blog_topic.strip():
            st.error("Please enter a blog topic.")
        else:
            with st.spinner("Writing your blog post..."):
                system = BLOG_SYSTEM.format(brand=brand, tone=tone.lower())
                user = BLOG_USER.format(
                    topic=blog_topic,
                    audience=blog_audience,
                    length=blog_length,
                    keywords=blog_keywords or "none specified",
                    sections=blog_sections,
                )
                # max_tokens scales with requested length (roughly 1.5 tokens/word + buffer)
                result = generate(system, user, temperature=temperature,
                                   max_tokens=int(blog_length * 1.5) + 300)
            save_to_history(result, "Blog Post", meta=blog_topic)
            render_result(result, "Blog Post", "blog_post")

# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — EMAIL GENERATOR
# ──────────────────────────────────────────────────────────────────────────────
with tab_email:
    st.subheader("📧 Email Generator")
    st.caption("Draft professional emails for any purpose, with adjustable formality.")

    c1, c2, c3 = st.columns(3)
    with c1:
        email_purpose = st.selectbox(
            "Purpose",
            ["Job Application", "Partnership Proposal", "Follow-Up", "Meeting Request",
             "Product Pitch", "Thank You Note", "Complaint / Issue Resolution",
             "Introduction", "Apology"],
            key="email_purpose",
        )
    with c2:
        email_recipient = st.text_input(
            "Recipient (role/relationship)",
            placeholder="e.g. HR Manager at TechCorp",
            key="email_recipient",
        )
    with c3:
        email_formality = st.select_slider(
            "Formality Level",
            ["Very Casual", "Casual", "Neutral", "Formal", "Very Formal"],
            value="Formal",
            key="email_formality",
        )

    email_context = st.text_area(
        "Context / Key Points to Include",
        height=120,
        placeholder="e.g. Following up on our call last week about the Q3 marketing campaign. "
                    "Want to confirm budget and propose a kickoff date.",
        key="email_context",
    )

    if st.button("Generate Email", type="primary", key="email_btn"):
        if not email_context.strip():
            st.error("Please add some context or key points for the email.")
        else:
            with st.spinner("Drafting your email..."):
                system = EMAIL_SYSTEM.format(brand=brand, tone=tone.lower())
                user = EMAIL_USER.format(
                    purpose=email_purpose,
                    recipient=email_recipient or "the recipient",
                    formality=email_formality,
                    context=email_context,
                )
                result = generate(system, user, temperature=max(temperature - 0.1, 0.0),
                                   max_tokens=600)
            save_to_history(result, "Email", meta=email_purpose)
            render_result(result, "Email", "email")


# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — SOCIAL MEDIA CONTENT
# ──────────────────────────────────────────────────────────────────────────────
with tab_social:
    st.subheader("📱 Social Media Content Generator")
    st.caption("Platform-specific posts — LinkedIn, Twitter/X, Instagram, WhatsApp.")

    c1, c2, c3 = st.columns(3)
    with c1:
        social_topic = st.text_input(
            "Topic / Message",
            placeholder="e.g. Launching our new AI-powered analytics dashboard",
            key="social_topic",
        )
    with c2:
        social_platform = st.selectbox(
            "Platform", list(PLATFORM_RULES.keys()), key="social_platform",
        )
    with c3:
        social_variations = st.number_input(
            "Number of Variations", min_value=1, max_value=5, value=3, key="social_variations",
        )

    with st.expander(f"Platform rules for {social_platform}"):
        st.info(PLATFORM_RULES[social_platform])

    c4, c5 = st.columns(2)
    with c4:
        social_emoji = st.checkbox("Include emojis", value=True, key="social_emoji")
    with c5:
        social_hashtags = st.checkbox("Include hashtags", value=True, key="social_hashtags")

    if st.button("Generate Posts", type="primary", key="social_btn"):
        if not social_topic.strip():
            st.error("Please enter a topic for the social media post.")
        else:
            with st.spinner(f"Creating {social_platform} content..."):
                extras = []
                extras.append("Use relevant emojis." if social_emoji else "Do not use emojis.")
                extras.append("Include relevant hashtags." if social_hashtags else "Do not include hashtags.")

                system = SOCIAL_SYSTEM.format(brand=brand, tone=tone.lower())
                user = SOCIAL_USER.format(
                    n_variations=social_variations,
                    platform=social_platform,
                    topic=social_topic,
                    platform_rules=PLATFORM_RULES[social_platform],
                    extra_instructions=" ".join(extras),
                )
                result = generate(system, user, temperature=min(temperature + 0.1, 1.5),
                                   max_tokens=200 * int(social_variations) + 200)
            save_to_history(result, f"{social_platform} Post(s)", meta=social_topic)
            render_result(result, f"{social_platform} Post(s)", "social_post")


# ──────────────────────────────────────────────────────────────────────────────
# TAB 4 — AD COPY GENERATOR
# ──────────────────────────────────────────────────────────────────────────────
with tab_ad:
    st.subheader("📣 Ad Copy Generator")
    st.caption("Headline, subheadline, body copy, and CTA for any campaign.")

    c1, c2 = st.columns(2)
    with c1:
        ad_product = st.text_input(
            "Product / Service", placeholder="e.g. SmartInvoice — AI invoicing tool",
            key="ad_product",
        )
        ad_audience = st.text_input(
            "Target Audience", placeholder="e.g. Small business owners in India",
            key="ad_audience",
        )
    with c2:
        ad_usp = st.text_input(
            "Unique Selling Point (USP)",
            placeholder="e.g. Generate invoices in 10 seconds with AI",
            key="ad_usp",
        )
        ad_cta = st.text_input(
            "Call to Action", placeholder="e.g. Start your free trial",
            key="ad_cta",
        )

    ad_platform = st.selectbox(
        "Ad Platform",
        ["Google Ads (Search)", "Facebook / Instagram Ads", "LinkedIn Ads", "Display Banner"],
        key="ad_platform",
    )

    if st.button("Generate Ad Copy", type="primary", key="ad_btn"):
        if not ad_product.strip() or not ad_usp.strip():
            st.error("Please fill in at least Product/Service and USP.")
        else:
            with st.spinner("Writing ad copy..."):
                system = AD_SYSTEM.format(brand=brand, tone=tone.lower())
                user = AD_USER.format(
                    product=ad_product,
                    usp=ad_usp,
                    audience=ad_audience or "general audience",
                    platform=ad_platform,
                    cta=ad_cta or "Learn More",
                )
                result = generate(system, user, temperature=temperature, max_tokens=400)
            save_to_history(result, "Ad Copy", meta=ad_product)
            render_result(result, "Ad Copy", "ad_copy")


# ──────────────────────────────────────────────────────────────────────────────
# TAB 5 — CONTENT TRANSLATOR
# ──────────────────────────────────────────────────────────────────────────────
with tab_translate:
    st.subheader("🌐 Content Translator")
    st.caption("Translate any generated content (or your own text) into Indian languages.")

    use_last = st.checkbox(
        "Translate the most recently generated content",
        value=bool(st.session_state.last_output),
        key="use_last_output",
    )

    if use_last and st.session_state.last_output:
        st.info("Using the most recently generated content (shown below, read-only).")
        st.text_area("Source content", st.session_state.last_output, height=150, disabled=True,
                      key="source_readonly")
        translate_source = st.session_state.last_output
    else:
        translate_source = st.text_area(
            "Paste content to translate",
            height=150,
            placeholder="Paste any text here to translate it...",
            key="translate_source_input",
        )

    target_languages = st.multiselect(
        "Translate to",
        TRANSLATION_LANGUAGES,
        default=["Hindi", "Telugu"],
        key="target_languages",
    )

    if st.button("Translate", type="primary", key="translate_btn"):
        if not translate_source.strip():
            st.error("Nothing to translate — generate some content first or paste text above.")
        elif not target_languages:
            st.error("Select at least one target language.")
        else:
            cols = st.columns(len(target_languages))
            combined_output = []
            for i, lang in enumerate(target_languages):
                with cols[i]:
                    st.markdown(f"**{lang}**")
                    with st.spinner(f"Translating to {lang}..."):
                        translated = translate(translate_source, lang)
                    st.write(translated)
                    st.download_button(
                        f"📥 Download {lang}",
                        translated,
                        file_name=f"translation_{lang.lower()}_{datetime.now().strftime('%H%M%S')}.txt",
                        mime="text/plain",
                        key=f"dl_translate_{lang}_{datetime.now().strftime('%H%M%S%f')}",
                    )
                    combined_output.append(f"--- {lang} ---\n{translated}")
            save_to_history("\n\n".join(combined_output), "Translation",
                             meta=", ".join(target_languages))


# ──────────────────────────────────────────────────────────────────────────────
# TAB 6 — ABOUT
# ──────────────────────────────────────────────────────────────────────────────
with tab_about:
    st.subheader("ℹ️ About this App")
    st.markdown(f"""
**ContentCo AI Writing Assistant** is an internal tool built for the {brand}
content team. It demonstrates a production-style, full-stack AI application
built with **Python + Streamlit + Groq API + Gemini API**.

### Features
| Feature | Description |
|---|---|
| 📝 Blog Post Generator | Topic, audience, length, SEO keywords, tone |
| 📧 Email Generator | Purpose, recipient, context, formality level |
| 📱 Social Media Content | Platform-specific posts (LinkedIn, Twitter/X, Instagram, WhatsApp) |
| 📣 Ad Copy Generator | Product, USP, target audience, call-to-action |
| 🌐 Content Translator | Translate any output into 5+ Indian languages |

### Bonus Features
- **Content History** — every generation this session is logged in the sidebar
- **Session Persistence** — `st.session_state` keeps your history while the app is open
- **Bulk Download** — download your entire session's content in one file
- **Brand Settings** — set brand name, tone, and creativity once, applied everywhere

### Architecture
```
ai_writing_assistant.py   <- main Streamlit app (this file)
utils/
    ai_client.py           <- Groq + Gemini API wrappers (cached clients)
    prompts.py             <- all prompt templates, editable in one place
.env                        <- your API keys (never commit this!)
requirements.txt            <- Python dependencies
```

### Tech Stack
- **Streamlit** — UI framework
- **Groq (`llama-3.3-70b-versatile`)** — fast text generation for blogs/emails/social/ads
- **Gemini (`gemini-2.5-flash`)** — translation engine (strong Indian language support)
- **python-dotenv** — loads API keys from `.env`

### For Students — Things to Try
1. Add a **6th content type** (e.g. Press Release) — copy the pattern from the Ad Copy tab.
2. Add a **"regenerate" button** that re-runs the same prompt with a different temperature.
3. Persist history to a file/database so it survives app restarts.
4. Add a **word/character counter** under each text area.
5. Swap Gemini for Groq's `mixtral-8x7b-32768` for translation and compare quality.
""")

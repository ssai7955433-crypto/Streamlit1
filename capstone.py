import streamlit as st
import json
from datetime import datetime
from utils.groq_client import generate, translate_content
from utils.prompts import PROMPTS
from dotenv import load_dotenv

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title='AI Writing Assistant',
    page_icon='✍️',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ── Session state init ────────────────────────────────────────────────────
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_output' not in st.session_state:
    st.session_state.last_output = ''

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.title('✍️ AI Writing Assistant')
    st.caption('ContentCo Internal Tool')
    st.divider()
    brand = st.text_input('Brand / Company Name', value='ContentCo')
    tone = st.selectbox('Default Tone',
                        ['Professional', 'Casual', 'Formal', 'Friendly', 'Persuasive'])
    temperature = st.slider('Creativity', 0.0, 1.5, 0.7, 0.1,
                            help='0=focused/factual 1.5=creative/varied')
    st.divider()
    st.metric('Content Generated Today', len(st.session_state.history))
    if st.button('🗑️ Clear History'):
        st.session_state.history = []
        st.rerun()

st.title('✍️ AI Writing Assistant')
st.caption(f'Powered by Groq AI · Brand: {brand} · Tone: {tone}')

# ── Tabs ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ['📝 Blog', '📧 Email', '📱 Social Media', '📢 Ad Copy', '🌐 Translate']
)


def save_and_display(content, content_type):
    st.session_state.last_output = content
    st.session_state.history.append({
        'type': content_type,
        'content': content,
        'time': datetime.now().strftime('%H:%M')
    })
    st.success(f'✅ {content_type} generated!')
    st.write(content)
    col1, col2 = st.columns(2)
    col1.download_button('📄 Download .txt', content,
                         f'{content_type.lower()}_{datetime.now().strftime("%H%M")}.txt',
                         mime="text/plain")
    col2.download_button('📄 Download .md', content,
                         f'{content_type.lower()}_{datetime.now().strftime("%H%M")}.md',
                         mime="text/markdown")


# TAB 1 — Blog Post
with tab1:
    st.subheader('📝 Blog Post Generator')
    c1, c2, c3 = st.columns(3)
    topic = c1.text_input('Topic', placeholder='AI in Indian Agriculture')
    audience = c2.selectbox('Audience',
                            ['General Public', 'Students', 'Professionals', 'Executives'])
    length = c3.select_slider('Length (words)', [300, 500, 800, 1200, 1500], value=800)
    keywords = st.text_input('SEO Keywords', placeholder='AI, farming, technology, India')
    sections = st.slider('Number of Sections', 3, 8, 4)
    if st.button('Generate Blog Post', type='primary', key='blog'):
        if topic:
            with st.spinner('Writing your blog post...'):
                prompt = PROMPTS['blog']['user'].format(
                    length=length, topic=topic, audience=audience,
                    tone=tone, keywords=keywords, sections=sections)
                result = generate(PROMPTS['blog']['system'], prompt, temperature, length*2)
                save_and_display(result, 'Blog Post')

# TAB 2 — Email
with tab2:
    st.subheader('📧 Email Generator')
    c1, c2 = st.columns(2)
    purpose = c1.selectbox('Purpose', ['Job Application', 'Partnership Proposal',
                                       'Follow-Up', 'Meeting Request', 'Product Pitch',
                                       'Thank You', 'Complaint'])
    recipient = c2.text_input('Recipient Role', placeholder='CEO, HR Manager, Client...')
    context = st.text_area('Your Context & Key Points', height=100,
                           placeholder='What do you want to communicate?')
    if st.button('Generate Email', type='primary', key='email'):
        if context:
            with st.spinner('Drafting your email...'):
                prompt = PROMPTS['email']['user'].format(
                    purpose=purpose, recipient=recipient, context=context, tone=tone)
                result = generate(PROMPTS['email']['system'], prompt, temperature-0.1, 600)
                save_and_display(result, 'Email')

# TAB 3 — Social Media
with tab3:
    st.subheader('📱 Social Media Content')
    c1, c2, c3 = st.columns(3)
    sm_topic = c1.text_input('Topic / Message')
    platform = c2.selectbox('Platform', ['LinkedIn', 'Twitter/X', 'Instagram', 'WhatsApp', 'YouTube'])
    num_posts = c3.number_input('Number of Post Variations', 1, 5, 3)
    use_emoji = st.checkbox('Include Emojis', value=True)
    use_tags = st.checkbox('Include Hashtags', value=True)
    char_map = {'LinkedIn': 3000, 'Twitter/X': 280, 'Instagram': 2200,
                'WhatsApp': 500, 'YouTube': 5000}
    if st.button('Generate Posts', type='primary', key='social'):
        if sm_topic:
            with st.spinner(f'Creating {num_posts} {platform} posts...'):
                prompt = f'''Create {num_posts} different {platform} post variations about: {sm_topic}
Brand: {brand}. Tone: {tone}. Character limit: {char_map[platform]}.
{"Include emojis." if use_emoji else ""}
{"Include 3-5 hashtags." if use_tags else ""}
Separate each variation with ---'''
                result = generate('You are a social media expert.', prompt, temperature+0.1, 1000)
                save_and_display(result, f'{platform} Posts')

# TAB 4 — Ad Copy
with tab4:
    st.subheader('📢 Ad Copy Generator')
    c1, c2 = st.columns(2)
    product = c1.text_input('Product / Service', placeholder='AI Writing Tool')
    usp = c2.text_input('Unique Selling Point', placeholder='10x faster content creation')
    c3, c4 = st.columns(2)
    ad_audience = c3.text_input('Target Audience', placeholder='Marketing professionals')
    cta = c4.text_input('Call to Action', placeholder='Start Free Trial')
    ad_platform = st.selectbox('Ad Platform', ['Google Ads', 'Facebook/Instagram',
                                               'LinkedIn Ads', 'Banner Ad'])
    if st.button('Generate Ad Copy', type='primary', key='ad'):
        if product:
            with st.spinner('Creating your ad copy...'):
                prompt = PROMPTS['ad']['user'].format(
                    product=product, usp=usp, audience=ad_audience,
                    platform=ad_platform, cta=cta, tone=tone)
                result = generate(PROMPTS['ad']['system'], prompt, temperature, 500)
                save_and_display(result, 'Ad Copy')

# TAB 5 — Translate
with tab5:
    st.subheader('🌐 Content Translator')
    use_last = st.checkbox('Translate last generated content', value=True)
    if use_last and st.session_state.last_output:
        to_translate = st.session_state.last_output[:2000]
        st.info('Using last generated content')
    else:
        to_translate = st.text_area('Paste content to translate', height=150)

    target_langs = st.multiselect('Translate to',
                                  ['Hindi', 'Telugu', 'Tamil', 'Bengali', 'Marathi',
                                   'Kannada', 'Malayalam', 'Gujarati'],
                                  default=['Hindi', 'Telugu'])
    if st.button('Translate All', type='primary', key='trans') and to_translate:
        cols = st.columns(len(target_langs) if target_langs else 1)
        for i, lang in enumerate(target_langs):
            with cols[i]:
                with st.spinner(f'Translating to {lang}...'):
                    result = translate_content(to_translate, lang)
                st.subheader(lang)
                st.write(result)
                st.download_button(f'📄 {lang}', result,
                                   f'content_{lang.lower()}.txt',
                                   key=f'dl_{lang}', mime="text/plain")

# ── History panel ─────────────────────────────────────────────────────────
if st.session_state.history:
    st.divider()
    with st.expander(f'🕑 Session History ({len(st.session_state.history)} items)'):
        for i, item in enumerate(reversed(st.session_state.history)):
            st.caption(f"{item['time']} — {item['type']}")
            st.write(item['content'][:200] + '...')
    st.divider()

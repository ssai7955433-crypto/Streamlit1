import streamlit as st 
import groq, os 
from dotenv import load_dotenv 
load_dotenv(dotenv_path=".env") 
@st.cache_resource 
def get_client(): 
 return groq.Groq(api_key=os.getenv('GROQ_API_KEY')) 
client = get_client() 
def groq_call(system, user, temp=0.7, tokens=600): 
 r = client.chat.completions.create(model='llama-3.3-70b-versatile', 
 messages=[{'role':'system','content':system},{'role':'user','content':user}],  temperature=temp, max_tokens=tokens) 
 return r.choices[0].message.content 
st.set_page_config(page_title='Team Productivity Hub', page_icon='⚡', layout='wide') 
st.title('⚡ Team Productivity Hub') 
with st.sidebar: 
 st.image('https://via.placeholder.com/200x60?text=Company+Logo')
 st.header('Settings') 
 tone = st.selectbox('Output Tone', ['Professional','Friendly','Concise','Detailed']) 
 language = st.selectbox('Output Language', ['English','Hindi','Telugu']) 
t1, t2, t3, t4 = st.tabs(['�� Summarizer','�� Email Reply','�� Meeting Notes','�� Translator']) 
# Tab 1 — Document Summarizer 
with t1: 
 st.subheader('Document Summarizer') 
 upload = st.file_uploader('Upload .txt file', type=['txt'], key='sum')
 manual = st.text_area('Or paste text here', height=200, key='sumtext')  
 text_input = upload.read().decode() if upload else manual 
 fmt = st.radio('Summary Format', ['Bullet Points','Executive Summary','Q&A Format'],  horizontal=True) 
 if st.button('Summarize', key='sb1', type='primary') and text_input: 
  with st.spinner(): 
    result = groq_call( 
 f'You are a {tone.lower()} document summarizer. Output in {language}.',  f'Summarize in {fmt}:\n{text_input[:4000]}', temp=0.4) 
  st.write(result) 
  st.download_button('Download', result, 'summary.txt', key='dl1') 
# Tab 2 — Email Reply Generator 
with t2: 
 st.subheader('Smart Email Reply Generator') 
 received = st.text_area('Paste received email', height=150) 
 reply_type = st.selectbox('Reply Type', ['Acknowledge','Approve','Decline','Request  more info','Schedule meeting']) 
 if st.button('Generate Reply', key='sb2', type='primary') and received: 
  with st.spinner():
    result = groq_call( 
 f'You write {tone.lower()} professional emails in {language}.',  f'Write a {reply_type} reply to:\n{received}', temp=0.6) 
  st.write(result) 
# Tab 3 — Meeting Notes 
with t3: 
 st.subheader('Meeting Notes Generator') 
 raw_notes = st.text_area('Paste rough meeting notes or transcript', height=200)  
if st.button('Structure Notes', key='sb3', type='primary') and  raw_notes:  
 with st.spinner(): 
   result = groq_call( 
 'You convert raw meeting notes into professional structured minutes.',  f'Structure these notes with: Attendees, Agenda, Key Decisions, Action  Items, Next Steps:\n{raw_notes}', temp=0.3) 
 st.write(result) 
# Tab 4 — Translator 
with t4: 
 st.subheader('Document Translator') 
 to_translate = st.text_area('Text to translate', height=150) 
 target_lang = st.selectbox('Translate to',  
['Hindi','Telugu','Tamil','French','Spanish','Japanese']) 
 if st.button('Translate', key='sb4', type='primary') and to_translate: 
  with st.spinner(): 
   result = groq_call( 
 f'You are an expert translator. Return ONLY the {target_lang}  translation.', 
 f'Translate to {target_lang}:\n{to_translate}', temp=0.2)   
   st.write(result) 

import streamlit as st 
import time 
st.set_page_config(page_title='AI Lab', page_icon='��', layout='wide') 
st.title('�� AI Lab — Day 3 Foundations') 
# ── Sidebar ─────────────────────────────────────────────────────────────── with st.sidebar: 
st.header('⚙️ Settings') 
model = st.selectbox('Model', ['llama3-70b (Groq)', 'gemini-1.5-flash']) 
temperature = st.slider('Temperature', 0.0, 2.0, 0.7, step=0.1) 
max_tokens = st.number_input('Max Tokens', 50, 2000, 500, step=50)  
st.divider() 
st.info(f'Model: {model}\nTemp: {temperature}\nTokens: {max_tokens}') 
# ── Two-column layout ───────────────────────────────────────────────────── col1, col2 = st.columns([2, 1]) 
col1,col2=st.columns([2,1])
with col1: 
 user_prompt = st.text_area('Enter your prompt', height=150, 
 placeholder='e.g. Explain machine learning in simple terms') 
 with col2: 
  task = st.selectbox('Task Type', ['General Q&A', 'Summarize', 'Translate', 'Explain']) 
  language = st.selectbox('Target Language', ['English', 'Hindi', 'Telugu', 'Tamil',  'French']) 
 include_emoji = st.checkbox('Add emojis to response', value=False) 
# ── Action Button ───────────────────────────────────────────────────────── if st.button('�� Generate', type='primary', use_container_width=True):  if not user_prompt.strip(): 
 if not user_prompt:
  st.error('⚠️ Please enter a prompt before generating!') 
 else: 
  with st.spinner(f'Running on {model}...'): 
   time.sleep(1) # Replace with real API call 
 result = f'[DEMO OUTPUT]\nTask: {task}\nPrompt: {user_prompt[:50]}...'  
 
 st.success('✅ Generated!') 
 st.write(result) 
 st.download_button('�� Download Result', result, file_name='output.txt') 
# ── Expander for instructions ───────────────────────────────────────────── with st.expander('�� How to use this app'): 
 st.write('1. Choose your model and settings in the sidebar') 
 st.write('2. Enter your prompt in the text area') 
 st.write('3. Select task type and target language')
 st.write('4. Click Generate') 

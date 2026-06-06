import streamlit as st
import time
import numpy as np

def do_something():
    print('Welcome to Streamlit')
st.title('My App') 
st.header('H2')
st.subheader('H3')
st.write('text, df, chart, dict — auto renders')
st.markdown('**Bold** and *italic*')
name = st.text_input('Your name', placeholder='e.g.  Aarav')
text = st.text_area('Paste text', height=200)
choice = st.selectbox('Pick one', ['A','B','C'])
temp = st.slider('Temperature', 0.0, 2.0, 0.7)
flag = st.checkbox('Include hashtags', value=True)
file = st.file_uploader('Upload', type=['txt','pdf'])
if st.button('Go', type='primary'): 
    do_something()
col1, col2 = st.columns(2)  
with col1: st.write('A')
with st.sidebar: st.header('Settings')
with st.expander('Show more'): st.write('details')

t1,t2 = st.tabs(['Tab1','Tab2']) 
with t1: st.write('...')

with st.spinner('Loading...'): time.sleep(2)
st.success('Done!') 
st.error('Failed!')
st.info('FYI')
with st.chat_message('user'): st.write('hello')
msg = st.chat_input('Type...')
st.session_state.messages = []


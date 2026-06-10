import streamlit as st 
import groq, os 
from dotenv import load_dotenv 
load_dotenv() 
@st.cache_resource 
def get_client(): 
 return groq.Groq(api_key=os.getenv('GROQ_API_KEY')) 
client = get_client() 
def ai(system, user, temp=0.6, tokens=700): 
 r = client.chat.completions.create(model='llama-3.3-70b-versatile',  messages=[{'role':'system','content':system},{'role':'user','content':user}],  temperature=temp, max_tokens=tokens) 
 return r.choices[0].message.content 
st.set_page_config(page_title='Marketing Automation', page_icon='��', layout='wide') 
st.title('�� Marketing Automation App') 
st.caption('Summarize → Translate → Generate Social Posts — all in one click') 
with st.sidebar: 
 brand = st.text_input('Brand Name', value='TechStartup') 
 industry = st.selectbox('Industry',  
['Technology','Healthcare','Education','Finance','Retail']) 
 target_langs = st.multiselect('Target Languages', 
 ['Hindi','Telugu','Tamil','Bengali','Marathi','Kannada'], 
 default=['Hindi','Telugu']) 
 platforms = st.multiselect('Social Platforms', 
 ['LinkedIn','Twitter/X','Instagram','WhatsApp'], 
 default=['LinkedIn','Twitter/X']) 
st.subheader('�� Input Content')
article = st.text_area('Paste article / press release / blog post', height=200,  placeholder='Paste any news article or marketing content here...') 
if st.button('�� Run Full Automation', type='primary', use_container_width=True): 
  if not article.strip(): 
   st.error('Please paste some content first!') 
else: 
 results = {} 
 # Step 1: Summarize 
 with st.spinner('Step 1/3: Summarizing content...'): 
  results['summary'] = ai(
   f'You are a marketing analyst for {brand} in {industry}.',  f'Summarize in 3 key bullet points for marketing use:\n{article[:3000]}',  temp=0.3) 
 # Step 2: Translate 
 with st.spinner(f'Step 2/3: Translating to {len(target_langs)} languages...'):  results['translations'] = {} 
 for lang in target_langs: 
  results['translations'][lang] = ai( 
 f'Translate accurately to {lang}. Return ONLY the translation.', results['summary'], temp=0.1) 
 # Step 3: Social Posts 
 with st.spinner('Step 3/3: Generating social media posts...'):  results['posts'] = {} 
 post_rules = { 
 'LinkedIn': 'professional, 150 words, include industry hashtags',  'Twitter/X': 'punchy, under 280 chars, max 3 hashtags',  'Instagram': 'engaging, use emojis, include caption and hashtags',  'WhatsApp': 'conversational, short, no hashtags' 
 } 
 for platform in platforms: 
  results['posts'][platform] = ai( 
 f'You create viral {platform} content for {brand}.', f'{post_rules[platform]}. Based on: {results["summary"]}', temp=0.8) 
 st.divider() 
 # Display: Summary 
 with st.expander('�� Summary', expanded=True): 
  st.write(results['summary']) 
 # Display: Translations 
 with st.expander('�� Translations', expanded=True): 
  t_cols = st.columns(len(target_langs)) 
 for i, lang in enumerate(target_langs): 
  t_cols[i].subheader(lang) 
 t_cols[i].write(results['translations'][lang]) 
 # Display: Social Posts 
 with st.expander('�� Social Media Posts', expanded=True): 
  p_cols = st.columns(len(platforms)) 
 for i, plat in enumerate(platforms): 
  p_cols[i].subheader(plat) 
 p_cols[i].code(results['posts'][plat], language=None) 
 st.success('✅ Automation complete! Processed in one click.') 

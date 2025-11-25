import streamlit as st
import pandas as pd 
import openai 
from openai import OpenAI
from os import getenv

st.set_page_config(
    page_title = 'ask for data',
    page_icon = '🥲',
    layout = 'wide'
)

#initialise client 
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=['OPENROUTER_API_KEY']
)
                       
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None
if "data_summary" not in st.session_state:
    st.session_state.data_summary = None
    


st.title('ask for data')
st.markdown('upload data and ask away')


with st.sidebar:
    st.header('data upload')
    uploaded_file = st.file_uploader('upload csv',type='csv')

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.success(f"loaded {df.shape[0]}")
            with st.expander('preview'):
                col1, col2 =st.columns(2)
                with col1:
                    st.metric("total rows", df.shape[0])
                
        except Exception as e:
            st.error(f'error:{str(e)}')
            st.info('make sure its a valid file bombaclaat')

    else:
        st.info('you havent uploaded yet!')

if st.session_state.df is not None:
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
    user_input = st.chat_input('ask about your data')

    if user_input:
        st.session_state.messages.append({'role':'user','content':user_input})
        with st.chat_message('user'):
            st.markdown(user_input)
    #PREPARE DATA CONTEXT
    df = st.session_state.df
    if len(df)> 100:
        data_context = f"""
        Dataset shape: {st.session_state.data_summary['shape']}
        Columns: {','.join(st.session_state.data_summary['columns'])}
        Data types: {st.session_state.data_summary['sample']}
        """
    else:
        data_context = f"""
        Full data:
        {df.to_string()}"""

    system_prompt = f""" you are a data analyst assistant. 

    the user has uploaded a csv file with the following information: {data_context}

    guidelines:
    1. answer the user's question clearly and concisely
    2. focus on providing specific answers 
    """
    with st.chat_message('assistant'):
        st.spinner('thinking...')
        try:
            response = client.chat.completions.create(
                model = 'openrouter/tngtech/deepseek-r1t2-chimera:free', #prefixed with openrouter/
                messages = [
                    {"role":"system", "content":system_prompt},
                    {"role":"user","content":user_input}
                ],
                temperature=0.1, max_tokens=800)
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({'role':'assistant','content':reply})
        except Exception as e:
            st.error(f'error generation response: {str(e)}')
            st.info('try again')
else:
    #no data
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info('upload csv file to start')
        st.markdown('example; what are the top 10 marriage goals?')
        
        

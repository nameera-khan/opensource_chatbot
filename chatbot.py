import streamlit as st

st.set_page_config(
    page_title = 'ask for data',
    page_icon = '🥲',
    layout = 'wide'
)
st.title('ask for data')
st.markdown('upload data and ask away')


with st.sidebar:
    st.header('data upload')
    uploaded_file = st.file_uploader('upload csv',type='csv')


import streamlit as st
import pandas as pd 

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

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
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
            
        

import os
import streamlit as st
import pandas as pd
import requests 
import json
# ------------------------------------------------------------------------------
# Streamlit Config
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Ask for Data",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------------------------------------------
# Set OpenRouter API Key safely
# ------------------------------------------------------------------------------
# Make sure your .streamlit/secrets.toml has:
# OPENROUTER_API_KEY = "or-xxxx-your-key"



# ------------------------------------------------------------------------------
# Initialize OpenRouter Client
# ------------------------------------------------------------------------------
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
 #   "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
  #  "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "tngtech/deepseek-r1t2-chimera:free",
    "messages": messages
    ]
  })
)



# ------------------------------------------------------------------------------
# UI State Initialization
# ------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df" not in st.session_state:
    st.session_state.df = None

# ------------------------------------------------------------------------------
# Title + Sidebar
# ------------------------------------------------------------------------------
st.title("Ask for Data")
st.markdown("Upload a CSV file and ask questions about it.")

with st.sidebar:
    st.header("Upload CSV")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.success(f"Loaded {df.shape[0]} rows.")

            with st.expander("Preview"):
                st.write(df.head())
        except Exception as e:
            st.error(f"Error loading CSV: {e}")
    else:
        st.info("No file uploaded yet.")

# ------------------------------------------------------------------------------
# Main Chat Logic
# ------------------------------------------------------------------------------
if st.session_state.df is not None:

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    user_input = st.chat_input("Ask about your data…")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        df = st.session_state.df

        # Build data context
        if len(df) > 100:
            data_context = f"""
Dataset shape: {df.shape}
Columns: {list(df.columns)}
Data types: {df.dtypes.to_dict()}
"""
        else:
            data_context = f"Full dataset:\n{df.to_string()}"

        system_prompt = f"""
You are a data analyst assistant.
The user uploaded a CSV file with this information:

{data_context}

Rules:
- Answer clearly and concisely
- Provide specific insights
- Use only the provided data
"""

        # Generate Answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]

                resp_json = response.json()
                reply = resp_json["choices"][0]["message"]["content"]

                if reply:
                    st.markdown(reply)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": reply}
                    )
                else:
                    st.error("Failed to generate response. Try again.")

else:
    st.info("Upload a CSV file to begin.")

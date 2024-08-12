import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Interactive Data Chat with Multiple LLMs")
st.title("Interactive Data Chat with Multiple LLMs 🤖📊")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'df' not in st.session_state:
    st.session_state.df = None

# Sidebar for file upload and LLM selection
st.sidebar.title("Configuration")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# LLM selection
llm_option = st.sidebar.selectbox(
    "Choose LLM",
    ("OpenAI", "Anthropic", "Ollama")
)

# LLM-specific configurations
if llm_option == "OpenAI":
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    if not openai_api_key.startswith("sk-"):
        st.sidebar.warning("Please enter a valid OpenAI API key!", icon="⚠️")
    openai_model = st.sidebar.selectbox("Select OpenAI Model", ["gpt-3.5-turbo", "gpt-4", "gpt-4-0125-preview"])
elif llm_option == "Anthropic":
    anthropic_api_key = st.sidebar.text_input("Anthropic API Key", type="password")
    if not anthropic_api_key.startswith("sk-"):
        st.sidebar.warning("Please enter a valid Anthropic API key!", icon="⚠️")
    anthropic_model = st.sidebar.selectbox("Select Anthropic Model", ["claude-3-haiku-20240307", "claude-3-sonnet-20240229"])
elif llm_option == "Ollama":
    ollama_model = st.sidebar.selectbox("Select Ollama Model", ["llama2", "mixtral"])

def process_response(response):
    if isinstance(response, dict):
        if 'value' in response:
            return response['value']
        elif 'type' in response and 'value' in response:
            return f"{response['type']}: {response['value']}"
    elif isinstance(response, str):
        try:
            json_response = json.loads(response)
            if isinstance(json_response, dict) and 'value' in json_response:
                return json_response['value']
        except json.JSONDecodeError:
            pass
    return str(response)

# Main content
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded data:")
    st.write(data.head(3))

    # Initialize LLM based on selection
    if llm_option == "OpenAI" and openai_api_key.startswith("sk-"):
        llm = ChatOpenAI(model=openai_model, openai_api_key=openai_api_key, temperature=0)
    elif llm_option == "Anthropic" and anthropic_api_key.startswith("sk-"):
        llm = ChatAnthropic(model=anthropic_model, anthropic_api_key=anthropic_api_key)
    elif llm_option == "Ollama":
        llm = Ollama(model=ollama_model)
    else:
        st.error("Please configure the selected LLM correctly.")
        st.stop()

    # Initialize SmartDataframe if not already done
    if st.session_state.df is None:
        st.session_state.df = SmartDataframe(data, config={"llm": llm})

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_input = st.chat_input("Ask a question about your data:")

    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.df.chat(user_input)
                    processed_response = process_response(response)
                    st.markdown(processed_response)
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": processed_response})
                except Exception as e:
                    error_message = f"An error occurred: {str(e)}"
                    st.error(error_message)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_message})

    # Option to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.experimental_rerun()

else:
    st.info("Please upload a CSV file to begin.")

# Add some information about the app
st.sidebar.markdown("---")
st.sidebar.info(
    "This app allows you to interactively chat with your CSV data using different LLMs. "
    "Upload a CSV file, select an LLM, and start asking questions about your data!"
)
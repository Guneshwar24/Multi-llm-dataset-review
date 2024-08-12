import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Interactive Data Chat with Multiple LLMs")
st.title("Interactive Data Chat with Multiple LLMs 🤖📊")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'data' not in st.session_state:
    st.session_state.data = None

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

def process_query(query, data):
    system_message = SystemMessage(content=f"""You are an AI assistant that helps users analyze CSV data. 
    The current dataframe has the following columns: {', '.join(data.columns)}. 
    When asked a question, provide a clear and concise answer based on the data. 
    If calculations or specific data manipulations are needed, explain the process in plain English.""")
    
    human_message = HumanMessage(content=f"Given the following query: '{query}', how would you answer this based on the available data?")
    
    messages = [system_message, human_message]
    
    response = llm(messages)
    return response.content

# Main content
if uploaded_file is not None:
    if st.session_state.data is None:
        st.session_state.data = pd.read_csv(uploaded_file)
    
    st.write("Preview of uploaded data:")
    st.write(st.session_state.data.head(3))

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
                    response = process_query(user_input, st.session_state.data)
                    st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
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
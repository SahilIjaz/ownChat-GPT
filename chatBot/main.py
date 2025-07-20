import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


def init():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("Please set the OPENAI_API_KEY environment variable.")
        exit(1)
    else:
        print("OPENAI_API_KEY is set.")

    st.set_page_config(page_title='Your own ChatGPT🫣',
                       page_icon='🫣')  # <- should be st.set_page_config

def main():
    init()

    st.header('Your own ChatGPT')

    chat = ChatOpenAI(temperature=0)

    # Use session state to persist messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content='You are a helpful assistant.')
        ]

    with st.sidebar:
        user_input = st.text_input("Enter your message:", key="user_input", placeholder="Type here...")

    if user_input:
        # Show user message
        message(user_input, is_user=True)
        st.session_state.messages.append(HumanMessage(content=user_input))

        # Get response from model
        response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

        # Show bot response
        message(response.content, is_user=False)

if __name__ == "__main__":
    main()


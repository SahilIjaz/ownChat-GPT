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

    st.set_page_config(page_title='Your own ChatGPT🫣', page_icon='🫣')

    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content='You are a helpful assistant.')
        ]


def extract_topic(text):
    """Return a brief summary to use as a sidebar history topic."""
    text = text.strip().split("?")[0]  
    return text[:40] + "..." if len(text) > 40 else text


def main():
    init()

    st.header('Your own ChatGPT')

    chat = ChatOpenAI(temperature=0)

    # Display full chat in the main area
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            message(msg.content, is_user=True)
        elif isinstance(msg, AIMessage):
            message(msg.content, is_user=False)

  
    with st.sidebar:
        st.subheader("Chat History 🧠")

      
        user_input = st.text_input("Ask something:", key="user_input", placeholder="Type here...")

        st.markdown("---")
        st.caption("Previous topics:")
        for msg in reversed(st.session_state.messages):
            if isinstance(msg, HumanMessage):
                topic = extract_topic(msg.content)
                st.markdown(f"• {topic}")

  
    if user_input:
  
        user_msg = HumanMessage(content=user_input)
        st.session_state.messages.append(user_msg)

        
        response = chat(st.session_state.messages)
        ai_msg = AIMessage(content=response.content)
        st.session_state.messages.append(ai_msg)

        
        st.experimental_rerun()


if __name__ == "__main__":
    main()

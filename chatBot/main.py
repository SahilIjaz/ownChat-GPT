# import streamlit as st
# from streamlit_chat import message
# from dotenv import load_dotenv
# import os
# from langchain_community.chat_models import ChatOpenAI
# from langchain.schema import SystemMessage, HumanMessage, AIMessage


# def init():
#     load_dotenv()
#     if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
#         print("Please set the OPENAI_API_KEY environment variable.")
#         exit(1)
#     else:
#         print("OPENAI_API_KEY is set.")

#     st.set_page_config(page_title='Your own ChatGPT🫣',
#                        page_icon='🫣')  # <- should be st.set_page_config

# def main():
#     init()

#     st.header('Your own ChatGPT')

#     chat = ChatOpenAI(temperature=0)

#     # Use session state to persist messages
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             SystemMessage(content='You are a helpful assistant.')
#         ]

#     with st.sidebar:
#         user_input = st.text_input("Enter your message:", key="user_input", placeholder="Type here...")

#     if user_input:
#         # Show user message
#         message(user_input, is_user=True)
#         st.session_state.messages.append(HumanMessage(content=user_input))

#         # Get response from model
#         response = chat(st.session_state.messages)
#         st.session_state.messages.append(AIMessage(content=response.content))

#         # Show bot response
#         message(response.content, is_user=False)

# if __name__ == "__main__":
#     main()


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

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            (HumanMessage(content='Hello! How are you?'), AIMessage(content='I am doing well, thank you! How can I assist you today?')),
            (HumanMessage(content='What is Python used for?'), AIMessage(content='Python is used for web development, data analysis, machine learning, scripting, and more.')),
            (HumanMessage(content='How do I fix a ModuleNotFoundError in Python?'), AIMessage(content='You can fix it by installing the missing module using pip, like `pip install module_name`.')),
            (HumanMessage(content='What is LangChain?'), AIMessage(content='LangChain is a framework to build applications powered by language models such as GPT-4.')),
            (HumanMessage(content='How do I load environment variables in Python?'), AIMessage(content='You can use the `python-dotenv` library and call `load_dotenv()` from dotenv.'))
        ]

def extract_topic(text):
    """Return a brief topic/summary string based on a user's question."""
    text = text.strip().split("?")[0]  # Get portion before question mark
    return text[:40] + "..." if len(text) > 40 else text

def main():
    init()

    st.header('Your own ChatGPT')

    # Display full conversation in the main area
    for human_msg, ai_msg in st.session_state.chat_history:
        message(human_msg.content, is_user=True)
        message(ai_msg.content)

    # Sidebar layout
    with st.sidebar:
        st.subheader("Your History 🧠")

        # Input field at the top
        user_input = st.text_input("Ask something:", key="user_input", placeholder="Type here...")

        st.markdown("---")
        st.caption("Previous topics:")
        for human_msg, _ in reversed(st.session_state.chat_history):
            topic = extract_topic(human_msg.content)
            st.markdown(f"• {topic}")

    # Handle user input
    if user_input:
        chat = ChatOpenAI(temperature=0)
        user_msg = HumanMessage(content=user_input)
        response = chat.invoke([SystemMessage(content="You are a helpful assistant."), user_msg])
        ai_msg = AIMessage(content=response.content)

        st.session_state.chat_history.append((user_msg, ai_msg))

        # Rerun to display new message
        st.experimental_rerun()

if __name__ == "__main__":
    main()

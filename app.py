import streamlit as st
from openai import OpenAI

# 1. Page Configuration & Layout
st.set_page_config(page_title="AI Course Assistant", page_icon="🤖")
st.title("🤖 AI Course Assistant")
st.write("Welcome! Ask me any questions about our AI Course Syllabus, policies, or deadlines.")

# 2. Sidebar for API Security
with st.sidebar:
    st.header("Setup Instructions")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.markdown("[Get OpenAI Key](https://openai.com)")

# 3. Initialize Conversation History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """You are the AI Assistant for ARTIFICIAL INTELLIGENCE BOOTCAMP]. 
            Here are the official rules for this specific course:
            - Assignment 1 Due: [16 MAY 2026]
            - Midterm Exam Date: [NOT APPLICABLE]
            - Final Project Due: [NA]
            - Grading Breakdown: Assignments are [NA]%, Midterm is [NA]%, Final Project is [NA]%.
            - Late Policy: [10% off per day late].
            - Professor Email: [-].
            If a student asks something not listed here, say: 'I don't have that information. Please ask the professor.'"""
        }
    ]


# 4. Display Existing Messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# 5. Handle User Input
if user_query := st.chat_input("Ask a question (e.g., 'What is the late policy?')"):
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar to talk to the bot!")
    else:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        # Generate AI response
        client = OpenAI(api_key=api_key)
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            
            ai_response = completion.choices[0].message.content
            response_placeholder.write(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})


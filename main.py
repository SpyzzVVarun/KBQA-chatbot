from openai import OpenAI
import time 

import streamlit as st
from streamlit_chat import message
from constants import *
from utils import *
from prompts import *

st.title("🦜🔗 Arxiv AI Assistant")

st.write("AI Assistant augmented with a Knowledge Base of ArXiv Papers. Supports updation of Knowledge Base.")

st.markdown("""
    <style>
    .footer {
        position: fixed;
        right: 0;
        bottom: 0;
        width: auto;
        background-color: transparent;
        color: white;
        text-align: right;
        padding-right: 20px;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="footer">Made by Varun Nagpal</p>', unsafe_allow_html=True)


# Sidebar
st.sidebar.title("Update Knowledge Base")

# File uploader widget
uploaded_file = st.sidebar.file_uploader("Add PDF of research paper ", type=['pdf', 'txt'])
url = st.sidebar.text_input("Enter arxiv page URL")
doi = st.sidebar.text_input("Entrer DOI")

# Submit button
submit_button = st.sidebar.button('Update Knowledge Base')

if submit_button:
    if uploaded_file or url or doi:
        with st.spinner('Updating Knowledge Base...'):
            time.sleep(5)
        st.success('Knowledge Base updated')
    else:
        st.sidebar.error("Please fill in at least one option.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"].replace("Question: ",""))

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt.replace("Question: ",""))
    context = find_match(prompt)
    st.session_state.messages.append({"role": "user", "content": "Question: " + prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages = [
    {"role": m["role"], "content": f"Context:\n {context} \n\n {m['content']}"}
    if m["content"] == "Question: "+ prompt else {"role": m["role"], "content": m["content"]}
    for m in st.session_state.messages
]
# {"role": m["role"], "content": f"Context:\n {context} \n\n Query:\n{prompt}"} 
,
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response.replace("Answer:","") + "▌")
        message_placeholder.markdown(full_response.replace("Answer:",""))
    st.session_state.messages.append({"role": "assistant", "content": full_response})
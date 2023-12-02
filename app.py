import time 
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

import streamlit as st
from streamlit_chat import message
from constants import *
from utils import *
from prompts import *

st.title("🦜🔗 Arxiv AI Assistant")

st.write("AI Assistant augmented with a Knowledge Base of ArXiv Papers. Supports updation of Knowledge Base.")
# Custom CSS to align text to the bottom right
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

# Adding the "Made by" text
st.markdown('<p class="footer">Made by Varun Nagpal</p>', unsafe_allow_html=True)


# Sidebar
st.sidebar.title("Update Knowledge Base")
# st.sidebar.subheader("Settings")

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
# if uploaded_file is not None:

# Adding widgets to the sidebar
# user_input = st.sidebar.text_input("Enter some text")
# number_input = st.sidebar.number_input("Enter a number", min_value=0, max_value=100, value=50)
# option = st.sidebar.selectbox("Choose an option", ["Option 1", "Option 2", "Option 3"])

# Initializing session state
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

if 'buffer_memory' not in st.session_state:
    st.session_state['buffer_memory'] = ConversationBufferWindowMemory(k=3,return_messages=True)

llm = ChatOpenAI(model_name=CHAT_MODEL, openai_api_key = OPENAI_API_KEY, streaming=True)
conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()

if not submit_button:
    with textcontainer:
        query = st.text_input("Query: ", key="input")
        if query:
            with st.spinner("typing..."):
                conversation_string = get_conversation_string()
                # refined_query = query_refiner(conversation_string, query)
                # st.subheader("Refined Query:")
                # st.write(refined_query)
                context = find_match(query)
                response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
            st.session_state.requests.append(query)
            st.session_state.responses.append(response) 
    with response_container:
        if st.session_state['responses']:
            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

    # if st.button('Refresh'):
    #     st.session_state['responses'] = ["How can I assist you?"]
    #     st.session_state['requests'] = []
    #     st.session_state['buffer_memory'] = ConversationBufferWindowMemory(k=3,return_messages=True)

            
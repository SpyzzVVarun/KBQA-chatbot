from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceBgeEmbeddings, OpenAIEmbeddings
import pinecone
import openai
import streamlit as st
from constants import *

openai.api_key = OPENAI_API_KEY
emb_model = OpenAIEmbeddings() # SentenceTransformer(EMB_MODEL)
pinecone.init(
    api_key= PINECONE_API_KEY,
	environment=ENV
)
index = pinecone.Index(index_name)

def find_match(input):
    input_em = emb_model.embed_query(input) #encode
    result = index.query(input_em, top_k=TOP_K, includeMetadata=True)
    context = ""
    for i in range(TOP_K):
       context += result['matches'][i]['metadata']['text']+"\n"
    return context

def query_refiner(conversation, query):

    response = openai.Completion.create(
        model=QUERY_MODEL,
        prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string

def get_similiar_docs(query,k=1,score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs
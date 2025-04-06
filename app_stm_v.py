# app_streamlit.py
import streamlit as st
import requests
import os
import json
from src import tools

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'config' not in st.session_state:
    st.session_state.config = {
        "salespersonName": "Deepika",
        "salespersonRole": "Energy Solutions Consultant",
        "companyName": "EcoTech Innovations",
        "companyBusiness": "Provides energy-efficient products...",
        "companyValues": "Promoting sustainability...",
        "conversationPurpose": "Help reduce energy bills...",
        "conversationType": "call",
        "withTools": True
    }

# Configuration Sidebar
with st.sidebar:
    st.header("Agent Configuration")
    
    new_config = {
        "salespersonName": st.text_input("Agent Name", st.session_state.config["salespersonName"]),
        "salespersonRole": st.text_input("Agent Role", st.session_state.config["salespersonRole"]),
        "companyName": st.text_input("Company Name", st.session_state.config["companyName"]),
        "companyBusiness": st.text_area("Company Business", st.session_state.config["companyBusiness"]),
        "companyValues": st.text_area("Company Values", st.session_state.config["companyValues"]),
        "conversationPurpose": st.text_input("Conversation Purpose", st.session_state.config["conversationPurpose"]),
        "conversationType": st.selectbox("Conversation Type", ["call", "chat"], index=0),
        "withTools": st.checkbox("Enable Tools", st.session_state.config["withTools"])
    }
    
    if st.button("Update Configuration"):
        st.session_state.config = new_config
        st.success("Configuration updated!")

# Main Interface
st.title("AI Call Agent Interface")

# Display conversation history
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("tools"):
            st.caption(f"Tools used: {msg['tools']}")

# User input
if user_input := st.chat_input("Type your message..."):
    # Add user message to history
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    # Process through agent (mimicking Flask's /upload_audio endpoint)
    try:
        # Step 1: Convert "audio" to text (direct text input)
        user_text = user_input
        
        # Step 2: Update conversation history
        conversation_history = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in st.session_state.conversation]
        )
        
        # Step 3: Handle tools
        tools_response = ""
        if st.session_state.config["withTools"]:
            tools_response_json = requests.post(
                "http://localhost:5000/conversation_tool",
                json={"conversation_history": conversation_history}
            ).json()
            
            if tools_response_json != "NO":
                tools_response = tools.get_tools_response(json.dumps(tools_response_json))
        
        # Step 4: Get agent response (mimicking /agent endpoint)
        agent_response = requests.post(
            "http://localhost:5000/agent",
            json={
                **st.session_state.config,
                "tools_response": tools_response,
                "conversation_history": conversation_history
            }
        ).json()
        
        # Process response
        clean_message = agent_response["message"]
        if agent_response["isEndOfCall"]:
            st.session_state.conversation = []
        
        # Add to history
        st.session_state.conversation.append({
            "role": "agent",
            "content": clean_message,
            "tools": tools_response if tools_response else None
        })
        
        st.rerun()
        
    except Exception as e:
        st.error(f"Error processing request: {str(e)}")

# Reset conversation
if st.button("Reset Conversation"):
    st.session_state.conversation = []
    st.rerun()
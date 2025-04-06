import streamlit as st
import agent
import src.tools
import os
from src.variables import CONVERSATION_STAGES

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'inputs' not in st.session_state:
    st.session_state.inputs = {}
if 'tools_response' not in st.session_state:
    st.session_state.tools_response = ""

# Configuration Form
with st.sidebar.form("config_form"):
    st.header("Agent Configuration")
    
    config = {
        "salesperson_name": st.text_input("Agent Name", "Deepika"),
        "salesperson_role": st.text_input("Agent Role", "Energy Solutions Consultant"),
        "company_name": st.text_input("Company Name", "EcoTech Innovations"),
        "company_business": st.text_area("Company Business", 
                    "Provides energy-efficient products like the EcoSmart Thermostat"),
        "company_values": st.text_area("Company Values",
                    "Promoting sustainability through innovative technologies"),
        "conversation_purpose": st.text_input("Conversation Purpose",
                    "Help prospects reduce energy bills with our thermostat"),
        "conversation_type": st.selectbox("Conversation Type", ["call", "chat"]),
        "use_tools": st.checkbox("Enable Tools", True)
    }
    
    if st.form_submit_button("Save Configuration"):
        st.session_state.inputs = config
        st.success("Configuration saved!")

# Main Chat Interface
st.title("AI Sales Agent")

# Display conversation history
for entry in st.session_state.conversation:
    with st.chat_message(entry["role"]):
        st.write(entry["content"])
        if entry.get("tools"):
            st.caption(f"Tools used: {entry['tools']}")

# User input
user_input = st.chat_input("Type your message...")
if user_input:
    # Add user message to history
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    # Process tools if enabled
    tools_response = ""
    if st.session_state.inputs.get("use_tools"):
        try:
            tools_response_json = agent.conversation_tool("\n".join(
                [f"{m['role']}: {m['content']}" for m in st.session_state.conversation]
            ))
            if tools_response_json != "NO":
                tools_response = src.tools.get_tools_response(tools_response_json)
        except Exception as e:
            st.error(f"Tool error: {str(e)}")
    
    # Generate agent response
    try:
        response = agent.sales_conversation_with_tools(
            st.session_state.inputs["salesperson_name"],
            st.session_state.inputs["salesperson_role"],
            st.session_state.inputs["company_name"],
            st.session_state.inputs["company_business"],
            st.session_state.inputs["company_values"],
            st.session_state.inputs["conversation_purpose"],
            st.session_state.inputs["conversation_type"],
            tools_response,
                "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.conversation])
            )
        
        # Clean response
        if "<END_OF_CALL>" in response:
            clean_message = response.split("<END_OF_CALL>")[0].strip()
            st.session_state.conversation = []  # Reset conversation
        elif "<END_OF_TURN>" in response:
            clean_message = response.split("<END_OF_TURN>")[0].strip()
        else:
            clean_message = response
            
        # Add agent response to history
        st.session_state.conversation.append({
            "role": "agent",
            "content": clean_message,
            "tools": tools_response if tools_response else None
        })
        
        # Rerun to update display
        st.rerun()
        
    except Exception as e:
        st.error(f"Agent error: {str(e)}")

# Add reset button
if st.button("Reset Conversation"):
    st.session_state.conversation = []
    st.rerun()
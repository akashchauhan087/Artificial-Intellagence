import streamlit as st
from ollama import chat

st.set_page_config(
    page_title="Ollama Chat",
    page_icon="🤖"
)

st.title("🤖 Local Ollama Chat")

MODEL_NAME = "llama3.2"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am running locally with Ollama 🚀"
        }
    ]

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask anything..."):

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        try:

            response = chat(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            full_response = response["message"]["content"]

            message_placeholder.markdown(full_response)

        except Exception as e:

            full_response = f"Error: {str(e)}"

            st.error(full_response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })

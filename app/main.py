import streamlit as st

from message_aggregator import MessageAggregator
from utils import converse_with_titan
from prepare_prompt import prepare_prompt

# Initialize aggregator
aggregator = MessageAggregator()

# Streamlit app
st.title("AI for Social Media Content and Conversation")

uploaded_files = st.file_uploader("Upload text or image files", type=["txt", "pdf", "png", "jpg"], accept_multiple_files=True)
keywords = st.text_input("Enter keywords:")
language = st.selectbox("Select language:", ["en", "uk"])
tone = st.selectbox("Select tone:", ["friendly", "formal", "creative"])


# Generate prompt
if st.button("Generate Content"):
    prompt = prepare_prompt(keywords.split(","), tone, language, uploaded_files)
    response, _ = converse_with_titan(prompt, [])
    st.text_area("Generated Content:", value=response, height=200)

# Chat interface
user_input = st.text_input("Enter your message:")
if st.button("Send Message"):
    aggregator.add_message("user", user_input)
    if aggregator.should_process("user"):
        aggregated_message = aggregator.get_aggregated_message("user")
        response, _ = converse_with_titan(aggregated_message, [])
        st.write("### AI Response")
        st.write(response)

import os
import streamlit as st
from io import BytesIO
from pypdf import PdfReader
from utils import process_uploaded_image, converse_with_titan
from prepare_prompt import prepare_prompt
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# App title
st.title("AI for Social Media Content Creation")

# Variables to store extracted data
image_labels = []
file_content = ""

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Files")
    uploaded_files = st.file_uploader(
        "Upload text or image files",
        type=["txt", "pdf", "png", "jpg"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            if file.type.startswith("image/"):
                # Process image to extract labels
                labels = process_uploaded_image(file)
                image_labels.extend(labels)
                st.success(f"Identified objects from {file.name}: {', '.join(labels)}")
            elif file.type in ["application/pdf", "text/plain"]:
                # Process text files to extract content
                content = ""
                if file.type == "application/pdf":
                    pdf_reader = PdfReader(BytesIO(file.read()))
                    content = "\n".join(page.extract_text() for page in pdf_reader.pages)
                else:
                    content = file.read().decode()
                file_content += f" {content.strip()} "
                st.success(f"Extracted content from {file.name}")

# Language and tone selection
language = st.selectbox("Select language:", ["en", "uk"])
tone = st.selectbox("Select tone:", ["friendly", "formal", "creative"])

# Input keywords for social media content
keywords = st.text_input("Enter keywords that describe your content:")

# Generate text button
if st.button("Generate Text"):
    if keywords or image_labels or file_content:
        # Prepare prompt using all extracted data
        prompt = prepare_prompt(
            keywords.split(","),
            tone,
            language,
            image_labels=image_labels,
            file_content=file_content
        )

        # Generate response using Bedrock
        response, _ = converse_with_titan(prompt, [])

        # Display results
        st.text_area("Generated Text:", value=response, height=200)

        # Debugging information (optional)
        st.write("### Debugging Info:")
        st.write(f"Prompt: {prompt}")
    else:
        st.warning("Please provide keywords, upload files, or upload images to generate content.")

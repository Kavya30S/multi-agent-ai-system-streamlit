import streamlit as st
import os
import json
import pdfplumber
from agents.classifier_agent import ClassifierAgent
from agents.email_agent import EmailAgent
from agents.json_agent import JsonAgent
from agents.memory_manager import MemoryManager

st.set_page_config(page_title="Multi-Agent AI System", page_icon="🤖")
st.title("Multi-Agent AI System")
st.write("Upload a file (TXT, JSON, or PDF) to process and classify its intent.")

# Initialize agents
classifier = ClassifierAgent()
email_agent = EmailAgent()
json_agent = JsonAgent()
memory_manager = MemoryManager()

# File upload
uploaded_file = st.file_uploader("Choose a file", type=["txt", "json", "pdf"])

if uploaded_file:
    # Save uploaded file temporarily
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read file content
    try:
        if uploaded_file.type == "text/plain":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        elif uploaded_file.type == "application/json":
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)
        elif uploaded_file.type == "application/pdf":
            with pdfplumber.open(file_path) as pdf:
                content = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        else:
            st.error("Unsupported file type.")
            content = None

        if content:
            # Classify intent
            intent = classifier.classify_intent(str(content))
            st.subheader("Classified Intent")
            st.write(intent)

            # Process based on file type
            result = {}
            thread_id = uploaded_file.name
            if uploaded_file.type == "text/plain":
                result = email_agent.process_email(thread_id, content)
            elif uploaded_file.type == "application/json":
                result = json_agent.process_json(thread_id, content)
            elif uploaded_file.type == "application/pdf":
                result = {"message": "PDF processed, extracted text stored in memory"}
                memory_manager.store_context({"thread_id": thread_id, "content": content})

            # Store in memory
            memory_manager.store_context({"thread_id": thread_id, "intent": intent, "result": result})

            # Display results
            st.subheader("Processing Results")
            st.json(result)

    except Exception as e:
        st.error(f"Error processing file: {e}")

    # Clean up
    if os.path.exists(file_path):
        os.remove(file_path)

if st.button("Clear Memory"):
    memory_manager.clear_memory()
    st.success("Memory cleared.")
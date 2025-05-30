Multi-Agent AI System (Streamlit)
This project is a Streamlit-based multi-agent AI system designed to process uploaded files (.txt, .json, .pdf), classify their intent (RFQ, Invoice, Complaint, Other), and extract relevant fields. It uses a modular agent architecture with ClassifierAgent for intent classification, EmailAgent for text emails, JsonAgent for JSON files, and MemoryManager for storing results in a SQLite database. The system integrates OpenRouter for fallback classification and is deployed locally and on Hugging Face Spaces for demonstration.

GitHub Repository: github.com/Kavya30S/multi-agent-ai-system-streamlit
Live Demo: Streamlit weInterface
Video Demo: Watch here

Project Overview
The system processes uploaded files via a Streamlit web interface:

Text Files (.txt): Treated as emails, extracting sender, subject, and urgency (High/Normal).
JSON Files (.json): Validates fields like invoice_number, amount, date, sender.
PDF Files (.pdf): Extracts text and stores it in the database.
Intent Classification: Uses a pre-trained BERT model (nlptown/bert-base-multilingual-uncased-sentiment) or OpenRouter API to classify intents.
Storage: Results are saved in memory/memory.db using SQLite.

This project was developed for an internship submission, demonstrating file processing, AI-driven classification, and web deployment.
Folder Structure
Below is the folder structure of the repository:
multi-agent-ai-system-streamlit/
├── agents/                     # Agent modules for processing and classification
│   ├── __init__.py            # Makes agents a Python package
│   ├── classifier_agent.py    # Handles intent classification (BERT/OpenRouter)
│   ├── email_agent.py         # Processes email text files
│   ├── json_agent.py          # Processes JSON files
│   └── memory_manager.py      # Manages SQLite database storage
├── demo/                      # Stores demo video
│   └── demo.mp4               # Video demo of the project
├── inputs/                    # Sample input files for testing
│   ├── complaint_email.txt    # Sample complaint email
│   ├── sample_email.txt       # Sample RFQ email
│   ├── sample_rfq.json        # Sample JSON invoice
│   ├── test_invalid.json      # Invalid JSON for error handling
│   └── sample_invoice.pdf     # Sample PDF invoice
├── memory/                    # SQLite database for storing results
│   └── memory.db              # Generated database (excluded by .gitignore)
├── temp/                      # Temporary folder for uploaded files
├── .gitignore                 # Specifies files to ignore in Git
├── app.py                     # Main Streamlit application
├── config.py                  # Configuration for API keys (excluded by .gitignore)
├── README.md                  # Project documentation (this file)
├── requirements.txt           # Python dependencies
├── test_classifier.py         # Test script for ClassifierAgent
├── test_email_agent.py        # Test script for EmailAgent
├── test_json_agent.py         # Test script for JsonAgent
└── test_openrouter.py         # Test script for OpenRouter API

Step-by-Step Setup Procedure
Follow these steps to set up and run the project locally on a Windows machine using Anaconda Prompt. The project requires Python 3.10 and an OpenRouter API key.
Prerequisites

Anaconda: Installed at C:\Users\<YourUsername>\anaconda3.
VS Code: Installed with Python extension.
Git: Installed for version control.
OpenRouter API Key: Obtain from openrouter.ai > Dashboard > Keys.


1. Clone the Repository

Open Anaconda Prompt.
Navigate to your desired directory:cd C:\Users\<YourUsername>\Documents


Clone the repository:git clone https://github.com/Kavya30S/multi-agent-ai-system-streamlit.git
cd multi-agent-ai-system-streamlit



2. Set Up Conda Environment

Create a Conda environment:conda create -n multi_agent_system python=3.10


Activate the environment:conda activate multi_agent_system


Install dependencies:pip install -r requirements.txt



3. Configure OpenRouter API Key

Create a .env file in the project root:OPENROUTER_API_KEY=sk-or-v1-your-actual-key

Replace sk-or-v1-your-actual-key with your OpenRouter key.
Ensure .gitignore includes .env to prevent pushing sensitive data.

4. Test Agents Locally

Test OpenRouter integration:python test_openrouter.py

Expected Output:hello


Test ClassifierAgent:python test_classifier.py

Expected Output:Intent: RFQ


Test EmailAgent:python test_email_agent.py

Expected Output:{'extracted_fields': {'sender': 'customer@example.com', 'subject': 'Request for Quotation', 'urgency': 'High'}, 'anomalies': []}


Test JsonAgent:python test_json_agent.py

Expected Output:{'extracted_fields': {'invoice_number': 'INV123', 'amount': 5000.0, 'date': '2025-05-29', 'sender': 'vendor@example.com'}, 'anomalies': []}



5. Run Streamlit App Locally

Launch the Streamlit app:streamlit run app.py


Open a browser and go to http://localhost:8501.
Upload sample files from inputs/ (e.g., complaint_email.txt):
Expected: Intent: Complaint, Results: {'extracted_fields': {'sender': 'support@clientcorp.com', ...}, 'anomalies': []}.


Check memory/memory.db in DB Browser for SQLite to verify stored results.


6. Record Video Demo

Install OBS Studio from obsproject.com.
Record a demo showing:
VS Code with app.py, classifier_agent.py.
Anaconda Prompt running streamlit run app.py.
Browser at http://localhost:8501 or Hugging Face Space URL.
File upload (e.g., complaint_email.txt).
DB Browser for SQLite showing memory/memory.db.


Narrate actions (optional, recommended) using a microphone.
Save as demo.mp4 in demo/ and push to GitHub.

Usage

Run the Streamlit app locally or access the live demo.
Upload a file (.txt, .json, .pdf) via the file uploader.
View the classified intent and extracted fields.
Use the “Clear Memory” button to reset the database.
Check memory/memory.db for stored results.

Troubleshooting

OpenRouter Errors: Verify OPENROUTER_API_KEY in config.py.
Incorrect Intents: Test ClassifierAgent with test_classifier.py and adjust intent_map if needed.
Database Issues: Ensure write permissions for memory/ folder.


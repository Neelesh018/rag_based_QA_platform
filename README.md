# RAG-Based QA Platform
---
## Features
- Upload and process up to 20 PDF documents simultaneously
- Query documents via a simple RESTful API
- Support for Google Gemini and OpenAI GPT models
- Easy local setup and Docker deployment
- Retrieve metadata about processed documents
- Automated testing with pytest
---
## Installation & Setup
### Clone the repository
git clone https://github.com/<Neelesh018>/rag-based-QA-platform.git
cd rag-based-QA-platform
### Setup virtual environment and activate
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
### Install dependencies
pip install -r requirements.txt
### Configure environment variables
Add your API keys to the environment:
GOOGLE_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_key
### Run the FastAPI server locally
uvicorn main:app --reload
### Docker Deployment
Start the container:
docker compose up --build
Stop the container:
docker compose down
---
## API Endpoints Overview
| Endpoint | HTTP Method | Description |
|----------------|-------------|-----------------------------------|
| `/process_pdfs`| POST | Upload and process up to 20 PDFs |
| `/query` | POST | Ask questions based on uploaded docs |
| `/metadata` | GET | Get metadata on processed documents |
---
## Running Tests
Run tests using:
pytest -v
---
## Configuring LLM Providers
### Using Google Gemini
from google import genai
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(prompt)
### Using OpenAI
import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
model="gpt-4o-mini",
messages=[{"role": "user", "content": prompt}]
)


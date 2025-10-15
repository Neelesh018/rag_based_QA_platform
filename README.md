# rag_based_QA_platform
###i. Setup & Installation Instructions

###----------- Clone the Repository ----------- 

git clone https://github.com/<Neelesh018>/rag-based-QA-platform.git

cd rag-based-QA-platform
### ----------- Create Virtual Environment -----------
###** python -m venv venv
###** source venv/bin/activate 
----------- Install Dependencies -----------
pip install -r requirements.txt
----------- Environment Variables -----------
GOOGLE_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_key
----------- Run Locally -----------
uvicorn main:app --reload
----------- Docker Deployment -----------
docker compose up --build
----------- Stop the Container -----------
docker compose down


ii. API Usage & Testing Guidelines
----------- Upload Documents -----------
Endpoint: POST /process_pdfs
Description: Upload and process up to 20 PDF files.
----------- Ask a Question -----------
Endpoint: POST /query
Description: Ask questions based on uploaded documents.
----------- View Metadata -----------
Endpoint: GET /metadata
Description: Retrieve details about processed documents.
----------- Run Tests -----------
pytest -v


iii. Configuration for Different LLM Providers
----------- Gemini (Google Generative AI) -----------
from google import genai
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(prompt)
----------- OpenAI -----------
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

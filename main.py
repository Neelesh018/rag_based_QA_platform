from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os, tempfile
from datetime import datetime
from app.app import get_pdf_text, get_text_chunks, create_vector_store, handle_query
from app.database import SessionLocal, DocumentMetadata

app = FastAPI(title="Gemini Multi-PDF RAG API")

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Upload PDFs
@app.post("/process_pdfs", response_class=PlainTextResponse)
async def process_pdfs(files: list[UploadFile]):
    if len(files) > 20:
        return PlainTextResponse("Maximum 20 PDFs allowed", status_code=400)
    db = SessionLocal()
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            all_text = ""
            for file in files:
                path = os.path.join(temp_dir, file.filename)
                content = await file.read()
                with open(path, "wb") as f:
                    f.write(content)
                all_text += get_pdf_text([open(path, "rb")]) + "\n"

                meta = DocumentMetadata(
                    filename=file.filename,
                    size_kb=round(len(content)/1024,2),
                    upload_time=datetime.utcnow(),
                    chunks=0
                )
                db.add(meta)

            chunks = get_text_chunks(all_text)
            create_vector_store(chunks)

            for meta in db.query(DocumentMetadata).all():
                meta.chunks = len(chunks)
            db.commit()
        return "Upload & processing done ✅"
    except Exception as e:
        db.rollback()
        return PlainTextResponse(f"Error: {e}", status_code=500)
    finally:
        db.close()

# Query PDFs
@app.post("/query")
async def query_pdf(question: str = Form(...)):
    try:
        answer = handle_query(question)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# View metadata
@app.get("/metadata")
def get_metadata():
    db = SessionLocal()
    try:
        docs = db.query(DocumentMetadata).all()
        return [
            {
                "filename": d.filename,
                "size_kb": d.size_kb,
                "upload_time": d.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
                "chunks": d.chunks
            }
            for d in docs
        ]
    finally:
        db.close()

import os
import pytest
from fastapi.testclient import TestClient
from main import app
from app.app import create_vector_store, get_text_chunks, handle_query

client = TestClient(app)

# Path to a small dummy PDF
SAMPLE_PDF = "tests/sample.pdf"

def test_process_pdfs_endpoint():
    with open(SAMPLE_PDF, "rb") as f:
        response = client.post("/process_pdfs", files={"files": ("sample.pdf", f, "application/pdf")})
    assert response.status_code == 200
    assert "Upload" in response.text

def test_metadata_endpoint():
    response = client.get("/metadata")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Each metadata entry should have filename and chunks
    if response.json():
        doc = response.json()[0]
        assert "filename" in doc
        assert "chunks" in doc

def test_query_endpoint():
    # Ensure some PDFs are uploaded first
    with open(SAMPLE_PDF, "rb") as f:
        client.post("/process_pdfs", files={"files": ("sample.pdf", f, "application/pdf")})
    
    # Test a query
    response = client.post("/query", data={"question": "What is this document about?"})
    assert response.status_code == 200
    json_resp = response.json()
    assert "answer" in json_resp

def test_vector_store_integration():
    text = "This is a test document for vector store integration."
    chunks = get_text_chunks(text)
    create_vector_store(chunks)
    result = handle_query("test document")
    assert isinstance(result, str)

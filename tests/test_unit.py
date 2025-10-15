import pytest
from app.app import get_text_chunks, get_pdf_text

def test_text_chunking():
    text = "This is a test document. " * 1000
    chunks = get_text_chunks(text)
    # Check that chunks are not empty
    assert len(chunks) > 0
    # Each chunk should be <= max chunk size
    for chunk in chunks:
        assert len(chunk) <= 10000 + 1000  # chunk_size + overlap

def test_pdf_text_extraction(tmp_path):
    # Create a dummy PDF
    pdf_path = tmp_path / "sample.pdf"
    pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
    pdf_path.write_bytes(pdf_content)

    text = get_pdf_text([open(pdf_path, "rb")])
    # Should return a string
    assert isinstance(text, str)

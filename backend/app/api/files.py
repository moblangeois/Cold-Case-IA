from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from app.models.schemas import DocumentInfo
from typing import List
import os

router = APIRouter()

CASE_DIR = "../Kyron_Horman"

@router.get("/documents", response_model=List[DocumentInfo])
async def list_documents(content_type: str = None):
    """
    List all documents in the case

    - **content_type**: Filter by content type (podcast_topics, scraped_sources, texts, official_documents, images)
    """
    documents = []

    # Define directories to scan
    scan_dirs = {
        "podcast_topics": os.path.join(CASE_DIR, "podcast_topics"),
        "scraped_sources": os.path.join(CASE_DIR, "scraped_sources"),
        "texts": os.path.join(CASE_DIR, "texts"),
        "official_documents": os.path.join(CASE_DIR, "official_documents"),
        "images": os.path.join(CASE_DIR, "images")
    }

    # Filter by content_type if specified
    if content_type:
        if content_type not in scan_dirs:
            raise HTTPException(status_code=400, detail="Invalid content_type")
        scan_dirs = {content_type: scan_dirs[content_type]}

    # Scan directories
    for ct, dir_path in scan_dirs.items():
        if not os.path.exists(dir_path):
            continue

        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)

            if not os.path.isfile(file_path):
                continue

            # Determine file type
            file_type = "unknown"
            preview = None

            if filename.endswith('.txt'):
                file_type = "text"
                # Read preview
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        preview = f.read(300).strip()
                except:
                    pass

            elif filename.lower().endswith('.pdf'):
                file_type = "pdf"

            elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_type = "image"

            # Get file size
            try:
                size = os.path.getsize(file_path)
            except:
                size = None

            documents.append(
                DocumentInfo(
                    filename=filename,
                    content_type=ct,
                    file_type=file_type,
                    size=size,
                    path=file_path.replace(CASE_DIR, ""),
                    preview=preview
                )
            )

    return documents

@router.get("/download/{content_type}/{filename}")
async def download_file(content_type: str, filename: str):
    """
    Download a specific file

    - **content_type**: Type of content
    - **filename**: Name of the file
    """
    # Build file path
    file_path = os.path.join(CASE_DIR, content_type, filename)

    # Security: prevent directory traversal
    if ".." in content_type or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid path")

    # Check if file exists
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=filename)

@router.get("/content/{content_type}/{filename}")
async def get_file_content(content_type: str, filename: str):
    """
    Get the content of a text file

    - **content_type**: Type of content
    - **filename**: Name of the file
    """
    # Build file path
    file_path = os.path.join(CASE_DIR, content_type, filename)

    # Security: prevent directory traversal
    if ".." in content_type or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid path")

    # Check if file exists
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Read file based on type
    if filename.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"filename": filename, "content": content, "type": "text"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    elif filename.lower().endswith('.pdf'):
        from PyPDF2 import PdfReader
        try:
            reader = PdfReader(file_path)
            all_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    all_text += text.strip() + "\n\n"
            return {"filename": filename, "content": all_text, "type": "pdf"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="File type not supported for content preview")

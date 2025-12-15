from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import CaseInfo, SearchRequest, SearchResult
from typing import List
import os

router = APIRouter()

CASE_DIR = "../Kyron_Horman"

@router.get("/", response_model=List[CaseInfo])
async def get_cases():
    """Get all available cases"""
    # For now, we only have Kyron Horman case
    # This can be extended to support multiple cases

    if not os.path.exists(CASE_DIR):
        return []

    # Count documents
    documents_count = 0
    images_count = 0
    texts_count = 0

    # Count official documents
    pdf_dir = os.path.join(CASE_DIR, "official_documents")
    if os.path.exists(pdf_dir):
        documents_count = len([f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')])

    # Count images
    img_dir = os.path.join(CASE_DIR, "images")
    if os.path.exists(img_dir):
        images_count = len([f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    # Count text files
    text_dirs = ["podcast_topics", "scraped_sources", "texts"]
    for text_dir in text_dirs:
        dir_path = os.path.join(CASE_DIR, text_dir)
        if os.path.exists(dir_path):
            texts_count += len([f for f in os.listdir(dir_path) if f.endswith('.txt')])

    return [
        CaseInfo(
            id="kyron_horman",
            name="Kyron Horman",
            description="Cold case investigation of the disappearance of Kyron Horman in Portland, Oregon, on June 4, 2010.",
            date="2010-06-04",
            location="Portland, Oregon, USA",
            status="open",
            documents_count=documents_count,
            images_count=images_count,
            texts_count=texts_count
        )
    ]

@router.get("/{case_id}", response_model=CaseInfo)
async def get_case(case_id: str):
    """Get details about a specific case"""
    cases = await get_cases()
    case = next((c for c in cases if c.id == case_id), None)

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    return case

@router.post("/search", response_model=List[SearchResult])
async def search_case(search_request: SearchRequest, app_request: Request):
    """
    Search within case documents

    - **query**: Search query
    - **case_id**: Case to search in
    - **limit**: Maximum number of results
    - **content_types**: Filter by content types
    """
    try:
        embeddings_service = app_request.app.state.embeddings_service

        results = await embeddings_service.search(
            query=search_request.query,
            n_results=search_request.limit,
            content_types=search_request.content_types
        )

        return [
            SearchResult(
                content=result["content"][:500],  # Preview only
                content_type=result["metadata"].get("content_type", "unknown"),
                filename=result["metadata"].get("filename", "unknown"),
                score=1 - result.get("distance", 0) if result.get("distance") is not None else 0.0,
                metadata=result["metadata"]
            )
            for result in results
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{case_id}/stats")
async def get_case_stats(case_id: str):
    """Get statistics about a case"""
    if case_id != "kyron_horman":
        raise HTTPException(status_code=404, detail="Case not found")

    stats = {
        "case_id": case_id,
        "total_documents": 0,
        "content_types": {},
        "file_types": {}
    }

    # Count files by type
    text_dirs = {
        "podcast_topics": os.path.join(CASE_DIR, "podcast_topics"),
        "scraped_sources": os.path.join(CASE_DIR, "scraped_sources"),
        "texts": os.path.join(CASE_DIR, "texts")
    }

    for content_type, dir_path in text_dirs.items():
        if os.path.exists(dir_path):
            count = len([f for f in os.listdir(dir_path) if f.endswith('.txt')])
            if count > 0:
                stats["content_types"][content_type] = count
                stats["total_documents"] += count

    # Count PDFs
    pdf_dir = os.path.join(CASE_DIR, "official_documents")
    if os.path.exists(pdf_dir):
        count = len([f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')])
        if count > 0:
            stats["content_types"]["official_documents"] = count
            stats["file_types"]["pdf"] = count
            stats["total_documents"] += count

    # Count images
    img_dir = os.path.join(CASE_DIR, "images")
    if os.path.exists(img_dir):
        count = len([f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        if count > 0:
            stats["content_types"]["images"] = count
            stats["file_types"]["images"] = count

    return stats

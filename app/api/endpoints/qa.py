import json
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.document_processor import process_document
from app.services.question_extractor import extract_questions
from app.services.question_answerer import answer_questions
from app.models.schemas import QAResponse

router = APIRouter()

@router.post("/qa", response_model=QAResponse)
async def qa_endpoint(
    document: UploadFile = File(...),
    questions: UploadFile = File(...)
):
    try:
        # Process the document
        doc_vectorstore = await process_document(document)
        
        # Extract questions from either JSON or PDF
        questions_list = await extract_questions(questions)
        
        # Answer the questions
        answers = await answer_questions(doc_vectorstore, questions_list)
        
        return QAResponse(results=answers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
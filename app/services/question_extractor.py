import json
from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader
import re

async def extract_questions(file: UploadFile) -> list:
    content = await file.read()
    if file.filename.endswith('.json'):
        return extract_questions_from_json(content)
    elif file.filename.endswith('.pdf'):
        return extract_questions_from_pdf(content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type for questions. Please upload a JSON or PDF file.")

def extract_questions_from_json(content: bytes) -> list:
    try:
        questions = json.loads(content.decode('utf-8'))
        if not isinstance(questions, list):
            raise HTTPException(status_code=400, detail="JSON file must contain an array of strings")
        return questions
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in questions file")

def extract_questions_from_pdf(content: bytes) -> list:
    try:
        reader = PdfReader(content)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # Simple regex to extract questions. This assumes questions end with a question mark.
        questions = re.findall(r'\b[A-Z][^.!?]*\?', text)
        
        if not questions:
            raise HTTPException(status_code=400, detail="No questions found in the PDF file")
        return questions
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing PDF file: {str(e)}")
import asyncio
import tempfile
import os
from fastapi import HTTPException, UploadFile
from langchain_community.document_loaders import PyPDFLoader, JSONLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter

async def process_document(file: UploadFile) -> Chroma:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        if file.filename.endswith('.pdf'):
            loader = PyPDFLoader(temp_file_path)
        elif file.filename.endswith('.json'):
            loader = JSONLoader(file_path=temp_file_path, jq_schema='.', text_content=False)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or JSON file.")
        
        documents = await asyncio.to_thread(loader.load)
        
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)
        
        print(f"Number of chunks created: {len(texts)}")
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(texts, embeddings)
        
        return vectorstore
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    finally:
        os.unlink(temp_file_path)
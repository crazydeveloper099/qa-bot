from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatAnthropic
from langchain.chains import RetrievalQA
from app.models.schemas import QuestionAnswer
from app.core.config import settings

async def answer_questions(vectorstore: Chroma, questions: List[str]) -> List[QuestionAnswer]:
    llm = ChatAnthropic(anthropic_api_key=settings.ANTHROPIC_API_KEY)
    
    # Dynamically determine the number of results to fetch
    k = determine_k(vectorstore, len(questions))
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": k})
    )
    
    answers = []
    for question in questions:
        try:
            result = qa_chain({"query": question})
            answers.append(QuestionAnswer(question=question, answer=result["result"]))
        except Exception as e:
            answers.append(QuestionAnswer(question=question, answer=f"Error processing this question: {str(e)}"))
    
    return answers

def determine_k(vectorstore: Chroma, num_questions: int) -> int:
    # Get the total number of chunks in the vectorstore
    total_chunks = len(vectorstore.get()['ids'])
    
    # Base k on the square root of total chunks, with a minimum of 3 and maximum of 10
    k = min(max(int(total_chunks ** 0.5), 3), 10)
    
    # Adjust k based on the number of questions
    if num_questions > 5:
        k = max(k - 1, 3)  # Reduce k slightly for many questions, but keep minimum of 3
    elif num_questions == 1:
        k = min(k + 1, 10)  # Increase k slightly for single questions, but keep maximum of 10
    
    return k
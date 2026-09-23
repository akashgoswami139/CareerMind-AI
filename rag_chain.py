from retriver import retriver
from prompt import prompts
from config import LLM_MODEL
from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL
)




def run_rag(user_query: str):
    # Retrieve relevant documents
    documents = retriver.invoke(user_query)

    # Combine retrieved documents into context
    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )

    # Build final prompt
    final_prompt = prompts.invoke(
        {
            "job_role": user_query,
            "context": context
        }
    )

    # Generate answer using Gemini
    response = llm.invoke(final_prompt)

    return response.content


# Only runs when you execute rag_chain.py directly
if __name__ == "__main__":
    user = input("Enter job role: ")
    response = run_rag(user)
    print(response)
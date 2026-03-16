from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

# Initialize the local LLM
model = OllamaLLM(model="llama3.2")

# Advanced Financial System Prompt
# Engineered for strict accuracy, professional tone, and clear formatting
template = """
You are the core intelligence engine of QuantRAG, a Senior Financial Analyst and Quantitative Strategist.

Your objective is to provide highly accurate, professional, and data-driven answers to the user's financial queries. 
You must rely strictly on the following retrieved financial records and market context to formulate your response:

--- RETRIEVED FINANCIAL DATA ---
{financial_context}
--------------------------------

User's Query: {question}

INSTRUCTIONS:
1. Analyze the retrieved financial data carefully.
2. Formulate a direct, structured, and professional response. Use bullet points if explaining complex concepts.
3. If the retrieved data does not contain the answer or is insufficient, DO NOT hallucinate or guess. Politely state: "Based on the available financial data in my system, I do not have enough specific information to answer this accurately."
4. Maintain an objective, expert tone at all times.

Expert Response:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

print("\n=======================================================")
print("  QuantRAG: Local Financial Analysis Agent Online")
print("=======================================================")

while True:
    print("\n-------------------------------------------------------")
    question = input("Enter your financial query (or 'q' to quit): ")
    print("-------------------------------------------------------\n")
    
    if question.lower() == "q":
        print("Shutting down QuantRAG. Goodbye.")
        break
    
    # 1. Retrieve the most relevant financial documents based on the query
    print("Retrieving market context...")
    retrieved_docs = retriever.invoke(question)
    
    # Format the retrieved documents into a single readable string for the LLM
    financial_context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # 2. Generate the expert response
    print("Synthesizing expert response...\n")
    result = chain.invoke({
        "financial_context": financial_context, 
        "question": question
    })
    
    print(result)
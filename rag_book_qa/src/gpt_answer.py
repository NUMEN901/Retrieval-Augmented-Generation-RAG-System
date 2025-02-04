import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("❌ OPENAI_API_KEY is not set!")

client = openai.OpenAI(api_key=api_key)

def generate_gpt_answer(query, retrieved_texts):
    """Uses OpenAI GPT to generate a **precise** answer based on retrieved text chunks."""
    if not retrieved_texts:
        return "⚠️ No relevant information found. Try rephrasing your question."

    context = "\n\n".join(retrieved_texts)

    prompt = f"""
    You are an AI assistant that **ONLY answers using the provided context**.

    **Question:** {query}

    **Context:** 
    {context}

    **Instructions:**  
    - **Give a short and precise answer (max 10 words).**  
    - **Do NOT provide explanations unless explicitly asked.**  
    - If the answer is a name, provide **only the name**.  
    - If the answer is a number (e.g., time, age, date), provide **only the number**.  
    - If comparing two facts (e.g., oldest character), **make the comparison directly**.  
    - If the information is incomplete, **explain what is missing**.  
    - If multiple relevant details exist, **synthesize into one short fact.**  

    **Answer:** 
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI that synthesizes information from multiple sources."},
                  {"role": "user", "content": prompt}],
        max_tokens=50  # Limit response length
    )

    return response.choices[0].message.content.strip()


from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .config import OLLAMA_MODEL

def create_analysis_chain():
    prompt_tempelate= """
    You are a helpful and non-judgmental cognitive coach. Your only role is to analyze the user's text for potential cognitive biases based on the provided list.

    **YOUR KNOWLEDGE BASE OF BIASES:**
    {bias_context}

    **USER'S REFLECTION TEXT:**
    {user_text}

    **YOUR TASK:**
    Analyze the user's reflection text. Identify up to three potential cognitive biases that may be influencing their reasoning. For each bias you identify, follow this format exactly:

    **Potential Bias:** [Name of the Bias]
    **Evidence:** "[Quote the exact sentence or phrase from the user's text that suggests this bias.]"
    **Explanation:** [Briefly and gently explain how this bias might be at play in their reasoning, referencing your knowledge base.]

    If you do not find any clear evidence of cognitive biases, respond with: "After reviewing your reflection, I did not find any clear examples of the cognitive biases from my knowledge base. Your reasoning appears to be quite balanced."
    """

    prompt=PromptTemplate(
        input_variables=["bias_context", "user_text"],
        template=prompt_tempelate,
    )

    llm=ChatOllama(model=OLLAMA_MODEL)
    output_parser=StrOutputParser()

    chain=prompt | llm | output_parser

    return chain
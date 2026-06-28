import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-flash-latest")

def get_ai_suggestions(resume_text):
    resume_text = resume_text[:3000]
    prompt = f"""
    You are an AI career assistant.

    Analyze this resume and give improvement suggestions:

    {resume_text}

    Give:
    - Skill improvements
    - Missing technologies
    - Career suggestions
    Keep it short and bullet points.
    """

    response = model.generate_content(prompt)
    return response.text
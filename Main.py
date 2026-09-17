import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="EduHub Academic AI API")

# Render Environment Variable থেকে API Key নিরাপদে লোড হবে
API_KEY = os.environ.get("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

class QueryRequest(BaseModel):
    course_code: str
    question: str
    context_text: str = ""

@app.get("/")
def home():
    return {"status": "EduHub Backend Active", "mode": "Online AI Enabled"}

@app.post("/api/chat")
def ask_ai(data: QueryRequest):
    try:
        prompt = f"""
        Role: Academic Assistant for Course {data.course_code}
        Context: {data.context_text[:4000]}
        Question: {data.question}
        
        Answer clearly in Bengali:
        """
        response = model.generate_content(prompt)
        return {"success": True, "answer": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import List, Optional
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI(
    title="JanAI API",
    description="Backend for JanAI AI Development Intelligence Platform",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class IssueSubmit(BaseModel):
    description: str
    category: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class IssueResponse(BaseModel):
    id: str
    description: str
    category: str
    ai_summary: str
    priority: str
    status: str

# --- Mock Database ---
MOCK_ISSUES = []

@app.get("/")
def read_root():
    return {"message": "Welcome to JanAI API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/issues", response_model=IssueResponse)
async def submit_issue(issue: IssueSubmit):
    ai_summary = f"Citizen reported: {issue.description[:50]}..."
    category = issue.category if issue.category else "Auto-detected: Infrastructure"
    priority = "Medium"
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Analyze this civic issue reported by a citizen: "{issue.description}"
        Respond in strict JSON format with exactly these keys:
        - "summary": A concise 1-sentence summary of the issue.
        - "category": One of [Roads & Infrastructure, Water Supply, Electricity, Sanitation, Other].
        - "priority": One of [Low, Medium, High, Critical] based on urgency and public impact.
        Do not include markdown blocks, just the JSON string.
        """
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"): text = text[7:]
        if text.endswith("```"): text = text[:-3]
        
        result = json.loads(text.strip())
        ai_summary = result.get("summary", ai_summary)
        category = result.get("category", category)
        priority = result.get("priority", priority)
    except Exception as e:
        print("Gemini API Error:", e)
        # Fallback to mock behavior if key is invalid or API fails
    
    new_issue = {
        "id": f"ISSUE-{len(MOCK_ISSUES)+1000}",
        "description": issue.description,
        "category": category,
        "ai_summary": ai_summary,
        "priority": priority,
        "status": "Pending Analysis"
    }
    MOCK_ISSUES.append(new_issue)
    return new_issue

@app.get("/api/issues", response_model=List[IssueResponse])
async def get_issues():
    return MOCK_ISSUES

@app.get("/api/analytics/summary")
async def get_analytics_summary():
    return {
        "total_feedback": 12450,
        "pending_issues": 2103,
        "resolved": 9842,
        "ai_impact_score": 8.4
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

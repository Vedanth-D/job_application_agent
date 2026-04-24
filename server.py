import asyncio
import json
import os
import io
import re
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    import fitz
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_text_from_docx(file_bytes: bytes) -> str:
    from docx import Document
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def build_fallback_suggestions(resume_text: str) -> dict:
    """Build basic suggestions from resume text without AI"""
    text_lower = resume_text.lower()
    skills = []
    skill_map = {
        "python": "Python", "java": "Java", "javascript": "JavaScript",
        "react": "React", "node": "Node.js", "sql": "SQL",
        "machine learning": "Machine Learning", "ml": "ML",
        "data science": "Data Science", "django": "Django",
        "fastapi": "FastAPI", "flask": "Flask", "docker": "Docker",
        "aws": "AWS", "cybersecurity": "Cybersecurity",
        "security": "Security", "networking": "Networking",
        "c++": "C++", "flutter": "Flutter", "android": "Android",
        "ios": "iOS", "devops": "DevOps", "kubernetes": "Kubernetes"
    }
    for key, val in skill_map.items():
        if key in text_lower:
            skills.append(val)

    skills = skills[:5] if skills else ["Communication", "Problem Solving", "Teamwork", "Analytical Thinking", "Programming"]

    # Detect experience level
    level = "Fresher"
    if any(w in text_lower for w in ["5+ years", "6 years", "7 years", "8 years", "senior", "lead", "manager"]):
        level = "Senior"
    elif any(w in text_lower for w in ["3 years", "4 years", "mid", "intermediate"]):
        level = "Mid-level"
    elif any(w in text_lower for w in ["1 year", "2 years", "junior", "associate"]):
        level = "Junior"

    # Build role suggestions based on detected skills
    suggestions = []
    if any(s in skills for s in ["Python", "FastAPI", "Django", "Flask"]):
        suggestions.append({
            "role": "Python Backend Developer",
            "reason": "Strong Python framework experience matches backend roles",
            "search_query": "python backend developer",
            "platforms": ["LinkedIn", "Remotive", "Naukri"]
        })
    if any(s in skills for s in ["Machine Learning", "ML", "Data Science"]):
        suggestions.append({
            "role": "Machine Learning Engineer",
            "reason": "ML and data science skills are highly in demand",
            "search_query": "machine learning engineer",
            "platforms": ["LinkedIn", "Remotive", "Indeed"]
        })
    if any(s in skills for s in ["Cybersecurity", "Security", "Networking"]):
        suggestions.append({
            "role": "Cybersecurity Analyst",
            "reason": "Security knowledge directly fits this role",
            "search_query": "cybersecurity analyst",
            "platforms": ["LinkedIn", "Indeed", "Naukri"]
        })
    if any(s in skills for s in ["React", "JavaScript", "Flutter"]):
        suggestions.append({
            "role": "Frontend Developer",
            "reason": "Frontend framework skills match web development roles",
            "search_query": "frontend developer react",
            "platforms": ["LinkedIn", "Internshala", "Remotive"]
        })
    if any(s in skills for s in ["Docker", "AWS", "DevOps", "Kubernetes"]):
        suggestions.append({
            "role": "DevOps Engineer",
            "reason": "Cloud and containerization skills fit DevOps roles",
            "search_query": "devops engineer cloud",
            "platforms": ["LinkedIn", "Remotive", "Naukri"]
        })

    # Fill up to 5 with generic roles
    generic = [
        {"role": "Software Engineer", "reason": "General software development skills match this role",
         "search_query": "software engineer", "platforms": ["LinkedIn", "Naukri"]},
        {"role": "Full Stack Developer", "reason": "Programming background suits full stack development",
         "search_query": "full stack developer", "platforms": ["LinkedIn", "Internshala"]},
        {"role": "API Developer", "reason": "Backend experience matches API development roles",
         "search_query": "api developer", "platforms": ["Remotive", "LinkedIn"]},
        {"role": "Junior Software Developer", "reason": "Good starting role for your experience level",
         "search_query": "junior software developer", "platforms": ["Internshala", "Naukri"]},
        {"role": "Technical Support Engineer", "reason": "Technical knowledge suits support engineering",
         "search_query": "technical support engineer", "platforms": ["LinkedIn", "Indeed"]},
    ]
    for g in generic:
        if len(suggestions) >= 5:
            break
        if not any(s["role"] == g["role"] for s in suggestions):
            suggestions.append(g)

    # Get candidate name
    lines = resume_text.strip().split("\n")
    name = "Candidate"
    for line in lines[:5]:
        line = line.strip()
        if line and len(line.split()) <= 4 and len(line) > 2:
            words = line.split()
            if all(w[0].isupper() for w in words if w.isalpha()):
                name = line
                break

    return {
        "name": name,
        "top_skills": skills,
        "experience_level": level,
        "suggestions": suggestions[:5]
    }

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename.lower()
    try:
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(contents)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(contents)
        elif filename.endswith(".txt") or filename.endswith(".md"):
            text = contents.decode("utf-8")
        else:
            return {"error": "Upload PDF, DOCX or TXT only."}
        if not text or len(text) < 30:
            return {"error": "Could not read text. Try a different format."}
        return {"text": text, "filename": file.filename}
    except Exception as e:
        return {"error": str(e)}

@app.post("/run-agent")
async def run_agent(query: str = Form(...), resume: str = Form(...)):
    async def generate():
        from agents.scraper import scraper_agent
        from agents.planner import planner_agent
        from agents.critic  import critic_agent
        from agents.writer  import writer_agent
        from agents.tracker import tracker_agent
        from core.state import AgentState

        state: AgentState = {
            "job_search_query": query,
            "resume_profile":   resume,
            "preferences":      {"remote": True},
            "listings":         [],
            "current_job":      None,
            "tailored_resume":  None,
            "cover_letter":     None,
            "applied_jobs":     [],
            "errors":           [],
            "status":           "starting"
        }

        def send(event, data):
            return f"data: {json.dumps({'event': event, 'data': data})}\n\n"

        yield send("stage", {"stage": "scraper", "message": "Searching LinkedIn, Internshala and Remotive..."})
        await asyncio.sleep(0.1)
        state = await asyncio.to_thread(scraper_agent, state)
        yield send("scraper_done", {
            "count": len(state["listings"]),
            "jobs":  [{"title": j["title"], "company": j["company"]}
                      for j in state["listings"]]
        })

        if not state["listings"]:
            yield send("done", {"message": "No jobs found. Try a different search term.", "total_applied": 0})
            return

        yield send("stage", {"stage": "planner", "message": "AI scoring each job against your resume..."})
        await asyncio.sleep(0.1)
        state = await asyncio.to_thread(planner_agent, state)
        yield send("planner_done", {
            "jobs": [{
                "title":   j["title"],
                "company": j["company"],
                "url":     j["url"],
                "source":  j.get("source", ""),
                "score":   j.get("fit_score", 0),
                "reason":  j.get("fit_reason", "")
            } for j in state["listings"]]
        })

        yield send("stage", {"stage": "critic", "message": "Selecting best matches..."})
        await asyncio.sleep(0.1)
        state = await asyncio.to_thread(critic_agent, state)
        approved = [j for j in state["listings"] if j.get("approved")]
        yield send("critic_done", {
            "approved_count": len(approved),
            "current_job": state["current_job"]["title"] if state["current_job"] else None
        })

        if state.get("current_job"):
            yield send("stage", {"stage": "writer",
                                  "message": f"Writing cover letter for {state['current_job']['title']}..."})
            await asyncio.sleep(0.1)
            state = await asyncio.to_thread(writer_agent, state)
            yield send("writer_done", {
                "job_title":       state["current_job"]["title"],
                "company":         state["current_job"]["company"],
                "job_url":         state["current_job"].get("url", "#"),
                "cover_letter":    state.get("cover_letter", ""),
                "tailored_resume": state.get("tailored_resume", "")
            })

            yield send("stage", {"stage": "tracker", "message": "Saving to log..."})
            await asyncio.sleep(0.1)
            state = await asyncio.to_thread(tracker_agent, state)
            yield send("done", {
                "message":       "Agent finished successfully!",
                "total_applied": len(state.get("applied_jobs", []))
            })
        else:
            yield send("done", {
                "message":       "No matching jobs found. Try a broader search.",
                "total_applied": 0
            })

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/suggest-jobs")
async def suggest_jobs(resume: str = Form(...)):
    from tools.llm import claude

    print(f"📋 Suggest: Resume length = {len(resume)} chars")

    # Always try AI first, fall back to keyword-based
    try:
        prompt = f"""You are a career advisor. Analyze this resume and suggest 5 job roles.

RESUME TEXT:
{resume[:1200]}

Return ONLY a JSON object. Start your response with {{ and end with }}.
No explanation, no markdown, no code blocks, just the raw JSON.

Use this structure:
{{
"name": "first name from resume",
"top_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
"experience_level": "Fresher",
"suggestions": [
{{"role": "Role 1", "reason": "short reason", "search_query": "search keywords", "platforms": ["LinkedIn", "Naukri"]}},
{{"role": "Role 2", "reason": "short reason", "search_query": "search keywords", "platforms": ["Remotive", "LinkedIn"]}},
{{"role": "Role 3", "reason": "short reason", "search_query": "search keywords", "platforms": ["Indeed", "Naukri"]}},
{{"role": "Role 4", "reason": "short reason", "search_query": "search keywords", "platforms": ["Internshala", "LinkedIn"]}},
{{"role": "Role 5", "reason": "short reason", "search_query": "search keywords", "platforms": ["LinkedIn", "Remotive"]}}
]
}}"""

        result = claude(prompt, max_tokens=800)
        print(f"📋 Suggest AI response: {result[:400]}")

        # Clean response
        result = result.strip()
        # Remove markdown
        result = re.sub(r'```json\s*', '', result)
        result = re.sub(r'```\s*', '', result)
        result = result.strip()

        # Find JSON boundaries
        start = result.find('{')
        end   = result.rfind('}')

        if start != -1 and end != -1 and end > start:
            json_str = result[start:end+1]
            data = json.loads(json_str)

            # Validate it has suggestions
            if "suggestions" in data and len(data["suggestions"]) > 0:
                print("✅ AI suggestions loaded successfully")
                return JSONResponse(content=data)

    except Exception as e:
        print(f"⚠️ AI suggest failed: {e} — using keyword fallback")

    # Fallback — keyword based, always works
    print("📋 Using keyword-based suggestions fallback")
    fallback = build_fallback_suggestions(resume)
    return JSONResponse(content=fallback)

@app.get("/applications")
async def get_applications():
    log_file = "data/applications.json"
    if os.path.exists(log_file):
        with open(log_file) as f:
            return json.load(f)
    return []

@app.delete("/applications/{job_id}")
async def delete_application(job_id: str):
    log_file = "data/applications.json"
    if os.path.exists(log_file):
        with open(log_file) as f:
            data = json.load(f)
        data = [d for d in data if d.get("id") != job_id]
        with open(log_file, "w") as f:
            json.dump(data, f, indent=2)
        return {"success": True}
    return {"success": False}

@app.delete("/applications")
async def delete_all_applications():
    with open("data/applications.json", "w") as f:
        json.dump([], f)
    return {"success": True}
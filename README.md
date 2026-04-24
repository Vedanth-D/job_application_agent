# 🤖 Job Agent — AI-Powered Job Application Assistant

An agentic AI system that automatically finds jobs from multiple platforms, scores them against your resume using AI, writes tailored cover letters, and helps you apply — all from a clean web dashboard.

---

## 📸 What It Does

1. **Upload your resume** (PDF, DOCX, or TXT)
2. **Type what job you want** — e.g. `python developer remote`
3. **Click Run Agent** — the AI pipeline runs automatically:
   - Scrapes jobs from **LinkedIn, Internshala, Remotive**
   - Scores each job against your resume using AI
   - Selects the best match
   - Writes a **tailored resume** and **cover letter**
   - Logs the application
4. **AI Suggestions** — instantly shows 5 roles you should apply for based on your resume

---

## 🏗️ Architecture — Multi-Agent Pipeline

```
Your Resume + Search Query
         │
         ▼
  ┌─────────────┐
  │   Scraper   │ ── Finds jobs from LinkedIn, Remotive, Internshala
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │   Planner   │ ── AI scores each job (0-100) against your resume
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │   Critic    │ ── Filters out low-score jobs, picks best match
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │   Writer    │ ── Writes tailored resume + cover letter using AI
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │   Tracker   │ ── Saves application log to JSON + Notion (optional)
  └─────────────┘
```

**Orchestrator:** LangGraph `StateGraph` routes between agents with conditional edges

---

## 📁 Project Structure

```
job-agent/
├── agents/
│   ├── scraper.py        # Finds jobs from multiple sources
│   ├── planner.py        # AI scores each job vs resume
│   ├── critic.py         # Filters and selects best job
│   ├── writer.py         # Writes cover letter + tailored resume
│   ├── browser.py        # Browser automation (optional)
│   └── tracker.py        # Logs applications
├── core/
│   ├── state.py          # Shared AgentState schema
│   ├── graph.py          # LangGraph orchestrator
│   └── memory.py         # Application memory/history
├── tools/
│   ├── llm.py            # Groq/Claude API wrapper
│   └── browser_tools.py  # Playwright helpers
├── static/
│   └── index.html        # Web dashboard UI
├── data/
│   └── applications.json # Application log
├── server.py             # FastAPI web server
├── main.py               # CLI entry point
├── .env                  # API keys (never commit this)
├── .gitignore
└── requirements.txt
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| AI / LLM | Groq (Llama 3.3 70B) — free |
| Web Framework | FastAPI + Uvicorn |
| Frontend | Vanilla HTML/CSS/JS |
| Job Sources | Remotive API, LinkedIn, Internshala |
| Resume Parsing | PyMuPDF (PDF), python-docx (DOCX) |
| Browser Automation | Playwright (optional) |
| Tracking | Local JSON + Notion API (optional) |

---

## 🚀 Setup — Step by Step

### Step 1 — Prerequisites

Make sure you have these installed:

- **Python 3.11+** → download from [python.org](https://python.org)
- **VS Code** → download from [code.visualstudio.com](https://code.visualstudio.com)
- **Git** → download from [git-scm.com](https://git-scm.com)

### Step 2 — Clone the Repository

```bash
git clone https://github.com/yourusername/job-agent.git
cd job-agent
```

### Step 3 — Create Virtual Environment

```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac/Linux
source venv/bin/activate
```

You should see `(venv)` appear in your terminal.

### Step 4 — Install Dependencies

```bash
pip install langgraph langchain-anthropic anthropic playwright \
            beautifulsoup4 requests notion-client python-dotenv \
            groq fastapi uvicorn python-multipart pymupdf python-docx
```

Then install the browser engine:

```bash
playwright install chromium
```

### Step 5 — Get API Keys

#### Groq API Key (Free — Required)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up free
3. Click **API Keys** → **Create API Key**
4. Copy the key starting with `gsk_...`

#### Notion API Key (Optional — for dashboard tracking)
1. Go to [notion.so/my-integrations](https://notion.so/my-integrations)
2. Click **New Integration** → name it `job-agent`
3. Copy the **Internal Integration Secret**
4. Create a Table database in Notion → connect your integration
5. Copy the database ID from the URL

#### Adzuna API Key (Optional — adds Naukri + Indeed jobs)
1. Go to [developer.adzuna.com](https://developer.adzuna.com)
2. Sign up free → Create Application
3. Copy `App ID` and `App Key`

### Step 6 — Create `.env` File

Create a file named `.env` in the root `job-agent/` folder:

```env
GROQ_API_KEY=gsk_your-groq-key-here
NOTION_API_KEY=secret_your-notion-key-here
NOTION_DATABASE_ID=your-database-id-here
ADZUNA_APP_ID=your-adzuna-app-id
ADZUNA_APP_KEY=your-adzuna-app-key
```

> ⚠️ Never share this file or push it to GitHub. It contains secret keys.

### Step 7 — Run the App

```bash
uvicorn server:app --reload
```

Then open your browser and go to:

```
http://127.0.0.1:8000
```

---

## 🖥️ How to Use

1. Open `http://127.0.0.1:8000` in your browser
2. **Upload your resume** — drag and drop or click to browse (PDF, DOCX, TXT)
3. AI instantly analyzes your resume and shows **5 job role suggestions** at the bottom
4. **Type your search** in the Job Search Query box — e.g. `cybersecurity analyst`
5. Click **RUN AGENT**
6. Watch the pipeline run live:
   - Pipeline steps light up one by one
   - Job cards appear with AI scores
   - Green border = approved jobs
   - Cover letter and tailored resume generated at the bottom
7. Click **View & Apply →** on any job card to open the real job page
8. Click **Copy** to copy your cover letter → paste it in the application form
9. Click **Open Job Page →** next to generated documents to go directly to apply

---

## 🔄 How to Run Again Later

Every time you want to start the project:

```bash
# Step 1 - go to project folder
cd D:\job-agent

# Step 2 - activate virtual environment
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Step 3 - start the server
uvicorn server:app --reload

# Step 4 - open browser
# Go to: http://127.0.0.1:8000
```

To stop the server press `Ctrl + C` in the terminal.

---

## 🤖 Agent Details

### Scraper Agent
Searches multiple job platforms simultaneously:
- **Remotive** — remote tech jobs via free API
- **LinkedIn** — public job listings (no login needed)
- **Internshala** — internships and fresher jobs in India
- **Adzuna** *(optional)* — aggregates Naukri + Indeed jobs

### Planner Agent
Uses Groq LLM (Llama 3.3 70B) to score each job 0-100 based on how well it matches your resume. Falls back to title-match scoring if descriptions are missing.

### Critic Agent
Acts as a quality gate — approves jobs scoring 50+ and skips ones you've already applied to.

### Writer Agent
Writes two documents for the best matching job:
- **Cover Letter** — 250-300 words, personalized to the company and role
- **Tailored Resume** — ATS-optimized version of your resume with keywords from the job description

### Tracker Agent
Saves every application to `data/applications.json` with timestamp and fit score. Optionally syncs to a Notion database.

---

## 📊 Features

| Feature | Status |
|---|---|
| Multi-source job scraping | ✅ |
| AI job scoring vs resume | ✅ |
| Tailored cover letter | ✅ |
| ATS-optimized resume | ✅ |
| Live streaming dashboard | ✅ |
| AI role suggestions from resume | ✅ |
| Application log (JSON) | ✅ |
| One-click apply button | ✅ |
| Notion sync | ✅ Optional |
| Browser auto-fill | ✅ Optional |

---

## 🛠️ Troubleshooting

**`venv\Scripts\activate` not working on Windows:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**`uvicorn` not recognized:**
```bash
pip install uvicorn
```

**API key error:**
- Make sure `.env` file exists in root folder
- No spaces around `=` sign
- No quotes around the key value

**No jobs found:**
- Try a simpler search term like `python developer`
- Check your internet connection
- LinkedIn sometimes blocks requests — Remotive always works

**Suggestions not loading:**
- The system uses keyword fallback automatically
- Even without AI, it reads your resume and suggests roles

---

## 🔐 Security Notes

- Your resume text is processed locally and sent only to Groq API for scoring
- API keys are stored in `.env` and never exposed to the frontend
- No user data is stored beyond `data/applications.json` on your machine
- The `.gitignore` file prevents `.env` from being pushed to GitHub

---

## 🚧 Future Improvements

- [ ] Gmail watcher — detect replies from companies
- [ ] Scheduled daily runs with cron job
- [ ] More job sources (Wellfound, WorkIndia)
- [ ] Interview preparation tips per job
- [ ] Application status tracking (Applied → Interview → Offer)
- [ ] Email notifications when new matching jobs appear

---

## 📄 License

Apache License 2.0 — free to use, modify and distribute with attribution.

---

## 🙋 Built By

Built as an agentic AI portfolio project demonstrating:
- Multi-agent orchestration with LangGraph
- Real-world tool use (web scraping, API calls, browser automation)
- Streaming server-sent events for live UI updates
- Production FastAPI backend with resume parsing

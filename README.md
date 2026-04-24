# 🤖 Job Agent — AI-Powered Job Application System

![Job Agent](https://img.shields.io/badge/JOB-AGENT-7c6af7?style=for-the-badge)
![Python](https://img.shields.io/badge/PYTHON-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FASTAPI-latest-009688?style=for-the-badge&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LANGGRAPH-agentic-orange?style=for-the-badge)
![Groq](https://img.shields.io/badge/GROQ-LLM-red?style=for-the-badge)
![LICENSE](https://img.shields.io/badge/LICENSE-Apache%202.0-green?style=for-the-badge)

> A full-stack Agentic AI system for automated job searching, resume tailoring, and cover letter generation across multiple job platforms.

- 🧠 AI-Powered | Multi-Agent Pipeline | LangGraph Orchestrated
- 🌐 Searches LinkedIn, Remotive, Internshala simultaneously
- 📄 Tailors your resume and writes cover letters automatically

---

## 📸 Project Screenshots

### 🖥️ Live Dashboard


![Dashboard](https://github.com/user-attachments/assets/bf8e653a-dbbc-492c-a2c6-94ad4bee860f)


---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Agent Pipeline](#-agent-pipeline)
- [Job Sources](#-job-sources)
- [API Keys Required](#-api-keys-required)
- [Troubleshooting](#-troubleshooting)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 📌 About the Project

**Job Agent** is a multi-agent AI application that automates the job application process end-to-end. Instead of manually browsing job boards and writing cover letters, this system does it all — finds jobs, scores them against your resume, writes tailored documents, and tracks applications.

Built using **LangGraph** for agent orchestration, **Groq LLM** for AI inference, and **FastAPI** for the backend — all accessible through a sleek real-time web dashboard.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 Multi-Source Scraping | Searches LinkedIn, Remotive, Internshala at once |
| 🧠 AI Job Scoring | Scores each job 0-100 against your resume |
| ✍️ Cover Letter Generation | Writes a 250-300 word personalized cover letter |
| 📄 Resume Tailoring | ATS-optimized resume with job-specific keywords |
| 💡 AI Role Suggestions | Suggests 5 roles based on your uploaded resume |
| 📊 Live Dashboard | Real-time streaming pipeline with job cards |
| 🔗 One-Click Apply | Opens real job pages with apply button |
| 📋 Application Log | Saves all applications to JSON + optional Notion sync |
| 🗑️ Clear Log | Delete saved applications from dashboard |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph StateGraph |
| AI / LLM | Groq — Llama 3.3 70B (Free) |
| Backend | FastAPI + Uvicorn |
| Frontend | HTML / CSS / Vanilla JS |
| Resume Parsing | PyMuPDF (PDF), python-docx (DOCX) |
| Job Sources | Remotive API, LinkedIn, Internshala |
| Optional Sources | Adzuna API (Naukri + Indeed aggregated) |
| Browser Automation | Playwright (optional) |
| Tracking | Local JSON + Notion API (optional) |
| Environment | Python 3.11+, Virtual Environment |

---

## 📁 Project Structure

```
job-agent/
├── agents/
│   ├── scraper.py        # Finds jobs from LinkedIn, Remotive, Internshala
│   ├── planner.py        # AI scores each job against your resume (0-100)
│   ├── critic.py         # Filters low scores, selects best match
│   ├── writer.py         # Writes tailored cover letter + resume
│   ├── browser.py        # Playwright browser automation (optional)
│   └── tracker.py        # Logs applications to JSON + Notion
│
├── core/
│   ├── state.py          # Shared AgentState TypedDict schema
│   ├── graph.py          # LangGraph orchestrator with routing
│   └── memory.py         # Application history and memory
│
├── tools/
│   ├── llm.py            # Groq API wrapper
│   └── browser_tools.py  # Playwright helper functions
│
├── static/
│   └── index.html        # Full web dashboard (single file)
│
├── data/
│   └── applications.json # Auto-generated application log
│
├── server.py             # FastAPI server with all endpoints
├── main.py               # CLI entry point (backup)
├── .env                  # Secret API keys — never commit this
├── .gitignore            # Ignores venv, .env, __pycache__
└── README.md             # This file
```

---

## 🔄 How It Works

```
 User uploads Resume (PDF/DOCX)
            │
            ▼
    ┌───────────────┐
    │  Scraper      │  →  Searches LinkedIn + Remotive + Internshala
    └──────┬────────┘
           │
           ▼
    ┌───────────────┐
    │  Planner      │  →  AI scores each job 0-100 vs your resume
    └──────┬────────┘
           │
           ▼
    ┌───────────────┐
    │  Critic       │  →  Approves jobs scoring 50+, skips duplicates
    └──────┬────────┘
           │
           ▼
    ┌───────────────┐
    │  Writer       │  →  Writes tailored resume + cover letter
    └──────┬────────┘
           │
           ▼
    ┌───────────────┐
    │  Tracker      │  →  Saves log to JSON + syncs to Notion
    └───────────────┘
           │
           ▼
    Dashboard shows job cards + generated documents
    User clicks "View & Apply →" to open real job page
```

**Orchestrator:** LangGraph `StateGraph` with conditional edges — routes to writer only if critic approves a job, otherwise exits cleanly.

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure these are installed on your machine:

- ✅ [Python 3.11+](https://python.org/downloads)
- ✅ [VS Code](https://code.visualstudio.com)
- ✅ [Git](https://git-scm.com)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/job-agent.git
cd job-agent
```

---

### Step 2 — Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv
```

```bash
# Activate — Windows
venv\Scripts\activate

# Activate — Mac / Linux
source venv/bin/activate
```

> ✅ You should see `(venv)` appear at the start of your terminal line

---

### Step 3 — Install All Dependencies

```bash
pip install langgraph langchain-anthropic anthropic playwright \
            beautifulsoup4 requests notion-client python-dotenv \
            groq fastapi uvicorn python-multipart pymupdf python-docx
```

Install the browser engine:

```bash
playwright install chromium
```

---

### Step 4 — Create `.env` File

Create a file named `.env` in the root `job-agent/` folder and paste:

```env
GROQ_API_KEY=gsk_your-groq-key-here
NOTION_API_KEY=secret_your-notion-key-here        # optional
NOTION_DATABASE_ID=your-database-id-here          # optional
ADZUNA_APP_ID=your-adzuna-app-id                  # optional
ADZUNA_APP_KEY=your-adzuna-app-key                # optional
```

> ⚠️ **IMPORTANT:** Never share this file. Never push it to GitHub. It is already listed in `.gitignore`.

---

### Step 5 — Run the Server

```bash
uvicorn server:app --reload
```

Open your browser and go to:

```
http://127.0.0.1:8000
```

---

## 🖥️ Usage

```
1.  Open http://127.0.0.1:8000
2.  Upload your resume — drag & drop or click to browse (PDF, DOCX, TXT)
3.  AI analyzes resume → shows 5 suggested roles at the bottom
4.  Type your job search → e.g. "cybersecurity analyst"
5.  Click RUN AGENT
6.  Watch the live pipeline:
    scraper → planner → critic → writer → tracker
7.  Job cards appear with AI scores (green border = approved)
8.  Cover letter + tailored resume shown at bottom
9.  Click "View & Apply →" to open the real job page
10. Click "Copy" → paste your cover letter into the application
```

---

## 🤖 Agent Pipeline

### 🔍 Scraper Agent
Searches multiple job platforms with your exact query:
- **Remotive** — remote tech jobs via free public API
- **LinkedIn** — public job listings without login required
- **Internshala** — internships and fresher jobs in India
- **Adzuna** *(optional)* — aggregates Naukri + Indeed + more

### 🧠 Planner Agent
Sends each job + your resume to Groq LLM for scoring. Returns a score 0-100 and a one-line reason. Falls back to title-match scoring if job description is missing.

### 🔎 Critic Agent
Quality gate — approves jobs scoring **50 or above**. Skips jobs already applied to. Picks the highest scoring job as the writing target.

### ✍️ Writer Agent
For the selected job, generates two documents:
- **Cover Letter** — 250-300 words, personalized to the role and company
- **Tailored Resume** — ATS-optimized with keywords from the job description

### 📋 Tracker Agent
Saves application details to `data/applications.json` with timestamp and fit score. Optionally syncs to a Notion database table.

---

## 🌐 Job Sources

| Platform | Type | Method |
|---|---|---|
| Remotive | Remote tech jobs worldwide | Free public API |
| LinkedIn | All job types, India focus | Public guest search |
| Internshala | Internships + fresher India | Web scraping |
| Adzuna *(optional)* | Naukri + Indeed aggregated | Free API key required |

---

## 🔑 API Keys Required

### Groq API — Free, Required
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up free
3. Click **API Keys** → **Create API Key**
4. Copy the key starting with `gsk_...`
5. Paste into `.env` as `GROQ_API_KEY`

### Adzuna API — Free, Optional (adds Naukri + Indeed)
1. Go to [developer.adzuna.com](https://developer.adzuna.com)
2. Sign up free → Create Application
3. Select Job Search, India as primary market
4. Copy `App ID` and `App Key` from dashboard
5. Paste into `.env` as `ADZUNA_APP_ID` and `ADZUNA_APP_KEY`

### Notion API — Free, Optional (application tracking dashboard)
1. Go to [notion.so/my-integrations](https://notion.so/my-integrations)
2. Create new integration → copy the Internal Integration Secret
3. Create a Table page in Notion → connect your integration via `...` menu
4. Copy the database ID from the URL
5. Paste into `.env` as `NOTION_API_KEY` and `NOTION_DATABASE_ID`

---

## 🔄 Running Again Later

Every time you want to start the project:

```bash
# Step 1 — go to project folder
cd D:\job-agent

# Step 2 — activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Step 3 — start the server
uvicorn server:app --reload

# Step 4 — open browser
# Go to: http://127.0.0.1:8000
```

Press `Ctrl + C` in terminal to stop the server.

---

## 🛠️ Troubleshooting

**`venv\Scripts\activate` fails on Windows:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**`uvicorn` not recognized:**
```bash
pip install uvicorn
```

**API authentication error:**
- Check `.env` file exists in root folder
- No spaces around `=` sign: `KEY=value` not `KEY = value`
- No quotes around the key values

**No jobs found:**
- Try a simpler search: `python developer` instead of very specific terms
- Remotive always works — LinkedIn may block requests occasionally
- Add Adzuna key for more consistent results

**Suggestions not loading:**
- System uses automatic keyword fallback
- Even without AI it reads your resume and suggests roles based on detected skills

---

## 🚀 Future Improvements

- [ ] Gmail watcher agent — detects company replies automatically
- [ ] Scheduled daily runs — cron job applies to new jobs every morning
- [ ] More job sources — Wellfound, WorkIndia, Shine
- [ ] Interview preparation tips generated per job role
- [ ] Application status tracker — Applied → Interview → Offer → Rejected
- [ ] Email notifications for new matching jobs
- [ ] Docker deployment for one-command setup

---

## 🎯 Interview Talking Points

When explaining this project, highlight these three concepts:

**1. Reflexion Pattern**
The Critic agent rejects low-fit jobs before the Writer wastes tokens — demonstrating self-evaluation in agentic systems.

**2. Conditional Edge Routing**
LangGraph routes to Writer only when Critic approves — showing production-level agent design with clean exit paths.

**3. Multi-Modal Pipeline**
Scraping + LLM scoring + document generation + live streaming UI — end-to-end system thinking beyond a simple chatbot.

---

## 👨‍💻 Author

Built as an Agentic AI portfolio project.

**LinkedIn:** [linkedin.com/in/vedanth-d-73a685296](https://linkedin.com/in/vedanth-d-73a685296)

---

## 📄 License

Apache License 2.0 — free to use, modify and distribute with attribution.

See [LICENSE](LICENSE) for full details.



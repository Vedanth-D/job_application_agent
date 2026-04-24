from tools.llm import claude
from core.state import AgentState

def writer_agent(state: AgentState) -> AgentState:
    job = state.get("current_job")
    if not job:
        print("✍️  Writer: No job to write for.")
        return {**state, "status": "done"}

    print(f"✍️  Writer: Writing for {job['title']} at {job['company']}...")

    resume_short = state["resume_profile"][:1200]
    desc_short   = job.get("description", "")[:600]

    # Cover letter — detailed version
    cl_prompt = f"""Write a professional and personalized cover letter for this job application.

JOB TITLE: {job['title']}
COMPANY: {job['company']}
JOB DESCRIPTION: {desc_short}

CANDIDATE PROFILE:
{resume_short}

Write a full cover letter with these 5 parts:
1. Strong opening line showing genuine interest in this specific company
2. What makes the candidate uniquely qualified — mention 2 specific skills or experiences from their profile
3. A concrete achievement or project from their background that directly matches this role
4. Why they want to work at this specific company and what they will contribute
5. Confident closing with call to action

Make it sound human, warm and specific — not generic. Length: 250-300 words.

Cover Letter:"""

    try:
        cover_letter = claude(cl_prompt, max_tokens=600)
        print("  ✅ Cover letter done")
    except Exception as e:
        print(f"  ⚠️ Cover letter error: {e}")
        cover_letter = f"""Dear Hiring Team at {job['company']},

I am writing to express my strong interest in the {job['title']} position at {job['company']}. Having carefully reviewed the job description, I am confident that my background and skills make me an excellent candidate for this role.

Throughout my career, I have developed strong expertise in areas directly relevant to this position. My hands-on experience with various technologies and projects has equipped me with both the technical skills and problem-solving mindset needed to excel in this role.

One of my key achievements includes building and delivering projects that demonstrate exactly the kind of initiative and technical depth your team is looking for. I take pride in writing clean, efficient code and collaborating effectively with cross-functional teams to deliver results on time.

What excites me most about {job['company']} is the opportunity to contribute to meaningful work while continuing to grow professionally. I am eager to bring my dedication and skills to your team and make a tangible impact from day one.

I would welcome the opportunity to discuss how my experience aligns with your needs. Thank you for considering my application — I look forward to hearing from you.

Warm regards,
{state['resume_profile'].split()[1] if len(state['resume_profile'].split()) > 1 else 'Candidate'}"""

    # Tailored resume
    resume_prompt = f"""Rewrite this resume to be ATS-optimized for the job below.
- Mirror keywords from the job naturally
- Put most relevant experience first
- Keep all real facts, just reorder and reword
- Output in clean plain text format

JOB: {job['title']} at {job['company']}
JOB KEYWORDS: {desc_short[:400]}

ORIGINAL RESUME:
{resume_short}

Tailored Resume:"""

    try:
        tailored = claude(resume_prompt, max_tokens=1000)
        print("  ✅ Resume tailored")
    except Exception as e:
        tailored = state["resume_profile"]
        print(f"  ⚠️ Resume fallback: {e}")

    return {
        **state,
        "tailored_resume": tailored,
        "cover_letter":    cover_letter
    }
from tools.llm import claude
from core.state import AgentState

def writer_agent(state: AgentState) -> AgentState:
    job = state.get("current_job")
    if not job:
        print("✍️  Writer: No job to write for, skipping.")
        return {**state, "status": "done"}

    print(f"✍️  Writer: Tailoring documents for {job['title']} at {job['company']}...")

    # --- Tailor the resume ---
    resume_prompt = f"""You are a professional resume writer.
Rewrite the resume below to be ATS-optimized for this specific job.
Rules:
- Mirror keywords from the job description naturally
- Reorder bullet points so most relevant ones come first  
- Do NOT add fake experience or skills
- Keep the same format, just reorder and reword
- Output the full resume in plain text

JOB TITLE: {job['title']}
COMPANY: {job['company']}
JOB DESCRIPTION:
{job['description'][:2000]}

ORIGINAL RESUME:
{state['resume_profile']}

Output the tailored resume now:"""

    try:
        tailored = claude(resume_prompt, max_tokens=2000)
        print("  ✅ Resume tailored")
    except Exception as e:
        print(f"  Resume tailoring failed: {e}")
        tailored = state["resume_profile"]

    # --- Write cover letter ---
    cl_prompt = f"""Write a professional cover letter for this job application.
Structure:
- Paragraph 1: Why you want THIS company specifically (not generic)
- Paragraph 2: 2 specific achievements from your experience that match the job
- Paragraph 3: Short closing with call to action

Keep it under 250 words. Sound human, not like AI.

JOB TITLE: {job['title']}
COMPANY: {job['company']}
JOB DESCRIPTION:
{job['description'][:1500]}

CANDIDATE BACKGROUND:
{state['resume_profile'][:800]}

Write the cover letter now:"""

    try:
        cover_letter = claude(cl_prompt, max_tokens=600)
        print("  ✅ Cover letter written")
    except Exception as e:
        print(f"  Cover letter failed: {e}")
        cover_letter = "Cover letter generation failed."

    return {
        **state,
        "tailored_resume": tailored,
        "cover_letter": cover_letter
    }
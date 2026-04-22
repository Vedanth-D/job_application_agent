import json
from tools.llm import claude
from core.state import AgentState

def planner_agent(state: AgentState) -> AgentState:
    print("🧠 Planner: Scoring job fits...")
    scored = []

    for job in state["listings"]:
        prompt = f"""Score this job fit for the candidate. 
Reply ONLY with valid JSON, no extra text, no markdown.

CANDIDATE PROFILE:
{state["resume_profile"][:1000]}

JOB TITLE: {job["title"]}
COMPANY: {job["company"]}
DESCRIPTION: {job["description"][:1500]}

Reply in this exact format:
{{"score": 75, "reason": "Strong Python match, missing AWS experience"}}"""

        try:
            result = claude(prompt, max_tokens=200)
            # Clean up response in case model adds extra text
            result = result.strip()
            if "{" in result:
                result = result[result.index("{"):result.rindex("}")+1]
            data = json.loads(result)
            scored.append({
                **job,
                "fit_score": data["score"],
                "fit_reason": data.get("reason", "")
            })
            print(f"  {job['title']} at {job['company']}: {data['score']}/100")
        except Exception as e:
            print(f"  Could not score {job['title']}: {e}")
            scored.append({**job, "fit_score": 0, "fit_reason": "scoring failed"})

    top = sorted(scored, key=lambda j: j["fit_score"], reverse=True)[:5]
    print(f"  Top pick: {top[0]['title']} ({top[0]['fit_score']}/100)" if top else "  No jobs scored")
    return {**state, "listings": top}
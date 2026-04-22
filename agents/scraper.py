import requests
from core.state import AgentState
import os

def scraper_agent(state: AgentState) -> AgentState:
    print("🔍 Scraper: Finding jobs...")
    
    query = state["job_search_query"]
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    listings = []

    try:
        # Adzuna API - works for India, shows real jobs
        url = (
            f"https://api.adzuna.com/v1/api/jobs/in/search/1"
            f"?app_id={app_id}&app_key={app_key}"
            f"&results_per_page=10"
            f"&what={query.replace(' ', '%20')}"
            f"&content-type=application/json"
        )
        res = requests.get(url, timeout=10)
        jobs = res.json().get("results", [])

        for job in jobs:
            listings.append({
                "id": str(job.get("id", "")),
                "title": job.get("title", ""),
                "company": job.get("company", {}).get("display_name", "Unknown"),
                "url": job.get("redirect_url", ""),
                "description": job.get("description", "")[:3000],
                "fit_score": None,
                "approved": None,
            })
        print(f"✅ Found {len(listings)} jobs from Adzuna")

    except Exception as e:
        print(f"Adzuna error: {e}")

    already_applied = state.get("applied_jobs", [])
    listings = [l for l in listings if l["id"] not in already_applied]
    return {**state, "listings": listings, "status": "evaluating"}
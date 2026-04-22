import os
import json
from datetime import datetime
from core.state import AgentState

def tracker_agent(state: AgentState) -> AgentState:
    print("📋 Tracker: Logging application...")
    job = state.get("current_job")
    if not job:
        return state

    log_entry = {
        "id": job["id"],
        "title": job["title"],
        "company": job["company"],
        "url": job["url"],
        "fit_score": job.get("fit_score", 0),
        "status": "applied",
        "date_applied": datetime.now().isoformat()
    }

    # Always save to local JSON
    os.makedirs("data", exist_ok=True)
    log_file = "data/applications.json"
    existing = []
    if os.path.exists(log_file):
        with open(log_file) as f:
            existing = json.load(f)
    existing.append(log_entry)
    with open(log_file, "w") as f:
        json.dump(existing, f, indent=2)
    print(f"  Saved to data/applications.json")

    # Try Notion if keys are set
    notion_key = os.getenv("NOTION_API_KEY")
    notion_db  = os.getenv("NOTION_DATABASE_ID")

    if notion_key and notion_db:
        try:
            from notion_client import Client
            notion = Client(auth=notion_key)
            notion.pages.create(
                parent={"database_id": notion_db},
                properties={
                    "Name":         {"title":  [{"text": {"content": job["title"]}}]},
                    "Company":      {"rich_text": [{"text": {"content": job["company"]}}]},
                    "URL":          {"url": job["url"]},
                    "Fit Score":    {"number": job.get("fit_score", 0)},
                    "Status":       {"select": {"name": "Applied"}},
                    "Date Applied": {"date": {"start": datetime.now().date().isoformat()}},
                }
            )
            print(f"  Synced to Notion")
        except Exception as e:
            print(f"  Notion sync failed (continuing anyway): {e}")

    print(f"✅ Logged: {job['title']} at {job['company']}")
    return {**state, "status": "done"}
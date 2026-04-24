import requests
import re
import os
from core.state import AgentState

def clean_html(text: str) -> str:
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def scraper_agent(state: AgentState) -> AgentState:
    print("🔍 Scraper: Finding jobs...")
    query         = state["job_search_query"].strip()
    query_encoded = requests.utils.quote(query)
    listings      = []
    already_applied = state.get("applied_jobs", [])

    # ── Source 1: Remotive (reliable free API) ─────────────────
    try:
        url  = f"https://remotive.com/api/remote-jobs?search={query_encoded}&limit=8"
        res  = requests.get(url, timeout=10)
        jobs = res.json().get("jobs", [])
        for job in jobs:
            listings.append({
                "id":          f"remotive_{job['id']}",
                "title":       job["title"],
                "company":     job["company_name"],
                "url":         job["url"],
                "source":      "Remotive",
                "description": clean_html(job.get("description", ""))[:2000],
                "fit_score":   None,
                "approved":    None,
            })
        print(f"  ✅ Remotive: {len(jobs)} jobs")
    except Exception as e:
        print(f"  ❌ Remotive: {e}")

    # ── Source 2: Adzuna India (Naukri + Indeed aggregated) ────
    adzuna_id  = os.getenv("ADZUNA_APP_ID", "")
    adzuna_key = os.getenv("ADZUNA_APP_KEY", "")
    if adzuna_id and adzuna_key:
        try:
            url  = (f"https://api.adzuna.com/v1/api/jobs/in/search/1"
                    f"?app_id={adzuna_id}&app_key={adzuna_key}"
                    f"&results_per_page=8&what={query_encoded}"
                    f"&content-type=application/json")
            res  = requests.get(url, timeout=12)
            jobs = res.json().get("results", [])
            for job in jobs:
                listings.append({
                    "id":          f"adzuna_{job['id']}",
                    "title":       job.get("title", ""),
                    "company":     job.get("company", {}).get("display_name", "Unknown"),
                    "url":         job.get("redirect_url", ""),
                    "source":      "Naukri/Indeed",
                    "description": job.get("description", "")[:2000],
                    "fit_score":   None,
                    "approved":    None,
                })
            print(f"  ✅ Naukri/Indeed via Adzuna: {len(jobs)} jobs")
        except Exception as e:
            print(f"  ❌ Adzuna: {e}")

    # ── Source 3: LinkedIn public guest search ─────────────────
    try:
        url = (f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
               f"?keywords={query_encoded}&location=India&start=0&count=8")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res     = requests.get(url, timeout=12, headers=headers)
        from bs4 import BeautifulSoup
        soup    = BeautifulSoup(res.text, "html.parser")
        cards   = soup.select("li")
        added   = 0
        seen    = set()
        for card in cards:
            try:
                title_el   = card.select_one(".base-search-card__title, h3")
                company_el = card.select_one(".base-search-card__subtitle, h4")
                link_el    = card.select_one("a.base-card__full-link, a[href*='linkedin.com/jobs']")
                if not title_el or not link_el: continue
                title   = title_el.get_text(strip=True)
                company = company_el.get_text(strip=True) if company_el else "Unknown"
                key     = f"{title}_{company}".lower()
                if key in seen: continue
                seen.add(key)
                job_url = link_el.get("href", "").split("?")[0]
                if not job_url: continue
                listings.append({
                    "id":          f"linkedin_{hash(job_url)}",
                    "title":       title,
                    "company":     company,
                    "url":         job_url,
                    "source":      "LinkedIn",
                    "description": f"{title} position at {company}.",
                    "fit_score":   None,
                    "approved":    None,
                })
                added += 1
                if added >= 6: break
            except:
                continue
        print(f"  ✅ LinkedIn: {added} jobs")
    except Exception as e:
        print(f"  ❌ LinkedIn: {e}")

    # ── Source 4: Internshala ──────────────────────────────────
    try:
        query_dashed = query.replace(" ", "-").lower()
        url     = f"https://internshala.com/internships/{query_dashed}-internship"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res     = requests.get(url, timeout=10, headers=headers)
        from bs4 import BeautifulSoup
        soup    = BeautifulSoup(res.text, "html.parser")
        cards   = soup.select(".individual_internship")[:5]
        added   = 0
        for card in cards:
            try:
                title_el   = card.select_one(".profile")
                company_el = card.select_one(".company_name, h4 a")
                link_el    = card.select_one("a[href*='/internship/detail'], a.view_detail_button")
                if not title_el: continue
                title   = title_el.get_text(strip=True)
                company = company_el.get_text(strip=True) if company_el else "Unknown"
                href    = link_el.get("href", "") if link_el else ""
                job_url = f"https://internshala.com{href}" if href.startswith("/") else url
                listings.append({
                    "id":          f"internshala_{hash(job_url)}",
                    "title":       title,
                    "company":     company,
                    "url":         job_url,
                    "source":      "Internshala",
                    "description": f"{title} internship at {company}.",
                    "fit_score":   None,
                    "approved":    None,
                })
                added += 1
            except:
                continue
        print(f"  ✅ Internshala: {added} jobs")
    except Exception as e:
        print(f"  ❌ Internshala: {e}")

    # ── Deduplicate ────────────────────────────────────────────
    seen_ids  = set()
    seen_keys = set()
    unique    = []
    for job in listings:
        key = f"{job['title'].lower().strip()}_{job['company'].lower().strip()}"
        if (job["id"] not in seen_ids and
            key not in seen_keys and
            job["id"] not in already_applied):
            seen_ids.add(job["id"])
            seen_keys.add(key)
            unique.append(job)

    print(f"✅ Total: {len(unique)} unique jobs")
    return {**state, "listings": unique, "status": "evaluating"}
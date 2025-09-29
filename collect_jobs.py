import requests
import json
from datetime import datetime

# ============================
# CONFIGURATION
# ============================
ALL_JOBS = []
OUTPUT_FILE = "real_jobs.json"  # JSON file to be used in your webpage
TODAY_DATE = datetime.now().strftime("%Y-%m-%d")
TIMEOUT = 10  # seconds for requests

# ============================
# FETCH FUNCTIONS
# ============================

def fetch_google_jobs():
    """Fetch India jobs from Google Careers (simplified)."""
    jobs = []
    try:
        url = "https://careers.google.com/api/v3/search/?location=India"
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()

        for job in data.get("jobs", []):
            jobs.append({
                "title": job.get("title", "N/A"),
                "company": "Google",
                "location": job.get("locations", [{}])[0].get("display", "N/A"),
                "description": "Tech, Engineering, and Business roles at Google India.",
                "apply_link": job.get("applyUrl") or job.get("detailsUrl", "#")
            })
        print(f"✅ Google: {len(jobs)} jobs found.")
    except Exception as e:
        print("❌ Google fetch failed:", e)
    return jobs

def fetch_lever_jobs():
    """Fetch India jobs from Zoho (Lever API)."""
    jobs = []
    try:
        url = "https://api.lever.co/v0/postings/zoho?mode=json"
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()

        for job in data:
            location = job.get("categories", {}).get("location", "")
            if "India" in location or "Remote" in location:
                jobs.append({
                    "title": job.get("text", "N/A"),
                    "company": "Zoho (via Lever)",
                    "location": location,
                    "description": "Various technical and non-technical roles. Filtered for India.",
                    "apply_link": job.get("hostedUrl", "#")
                })
        print(f"✅ Zoho (Lever): {len(jobs)} jobs found.")
    except Exception as e:
        print("❌ Lever fetch failed:", e)
    return jobs

def fetch_greenhouse_jobs():
    """Fetch India jobs from Stripe (Greenhouse API)."""
    jobs = []
    try:
        url = "https://boards-api.greenhouse.io/v1/boards/stripe/jobs"
        r = requests.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()

        for job in data.get("jobs", []):
            location = job.get("location", {}).get("name", "")
            if "India" in location or "Remote" in location:
                jobs.append({
                    "title": job.get("title", "N/A"),
                    "company": "Stripe (via Greenhouse)",
                    "location": location,
                    "description": "Fintech and software roles for Stripe.",
                    "apply_link": job.get("absolute_url", "#")
                })
        print(f"✅ Stripe (Greenhouse): {len(jobs)} jobs found.")
    except Exception as e:
        print("❌ Greenhouse fetch failed:", e)
    return jobs

def fetch_workday_jobs():
    """Fetch India jobs from Accenture (Workday) - simple GET fallback."""
    jobs = []
    try:
        url = "https://accenture.wd3.myworkdayjobs.com/wday/cxs/accenture/Accenture_Careers/jobs"
        headers = {"Accept": "application/json"}
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()

        for job in data.get("jobPostings", []):
            location = job.get("locationsText", "")
            if "India" in location or "Remote" in location:
                apply_link = "https://accenture.wd3.myworkdayjobs.com/en-US/Accenture_Careers/job/" + job.get("externalPath", "")
                jobs.append({
                    "title": job.get("title", "N/A"),
                    "company": "Accenture (via Workday)",
                    "location": location,
                    "description": "Consulting and Technology roles in India.",
                    "apply_link": apply_link
                })
        print(f"✅ Accenture (Workday): {len(jobs)} jobs found.")
    except Exception as e:
        print("❌ Workday fetch failed:", e)
    return jobs

# ============================
# MAIN EXECUTION
# ============================

def run_scraper():
    all_jobs = []
    all_jobs.extend(fetch_google_jobs())
    all_jobs.extend(fetch_lever_jobs())
    all_jobs.extend(fetch_greenhouse_jobs())
    all_jobs.extend(fetch_workday_jobs())

    # Convert to final structure for JSON
    final_jobs = []
    for i, job in enumerate(all_jobs):
        final_jobs.append({
            "id": i + 1,
            "title": job.get("title", "Unknown Role"),
            "company": job.get("company", "External Source"),
            "location": job.get("location", "India"),
            "description": job.get("description", "Click the link to view full details and apply."),
            "link": job.get("apply_link", "#"),
            "postedDate": TODAY_DATE
        })
    return final_jobs

# ============================
# SAVE TO JSON
# ============================

if __name__ == "__main__":
    jobs_data = run_scraper()
    # Save JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs_data, f, indent=2, ensure_ascii=False)
    print(f"\n✅ COLLECTED {len(jobs_data)} JOBS. Saved to {OUTPUT_FILE}.")

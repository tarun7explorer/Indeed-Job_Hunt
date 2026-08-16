import urllib.parse
from browser.selectors import Selectors
from browser.browser_manager import human_delay

class JobCollector:
    def __init__(self, page):
        self.page = page

    def build_search_urls(self, target_roles, locations, max_age_days=3):
        urls = []
        base_url = "https://in.indeed.com/jobs"
        
        for role in target_roles:
            for loc in locations:
                params = {
                    "q": role,
                    "l": loc,
                    "fromage": str(max_age_days),  # Only listings posted in last 3 days
                    "sc": "0kf:explvl(ENTRY_LEVEL);" # Entry Level / 0-2 YOE
                }
                if loc.lower() == "remote":
                    params["q"] = f"{role} remote"
                    params["l"] = ""
                
                url = f"{base_url}?{urllib.parse.urlencode(params)}"
                urls.append((role, loc, url))
        return urls

    def fetch_jobs_from_url(self, search_url):
        print(f"[COLLECTOR] Navigating to: {search_url}")
        self.page.goto(search_url)
        human_delay(3, 5)
        cards = self.page.locator(Selectors.JOB_CARD).all()
        print(f"[COLLECTOR] Found {len(cards)} fresh listings on this page.")
        return cards
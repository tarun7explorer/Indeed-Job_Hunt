import json
import os
from datetime import datetime

APPLIED_FILE = "data/applied_jobs.json"

class Tracker:
    def __init__(self):
        self.data = self._load()

    def _load(self):
        if not os.path.exists(APPLIED_FILE):
            return {}
        try:
            with open(APPLIED_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def is_processed(self, job_id):
        status = self.data.get(job_id, {}).get("status", "NEW")
        return status in ["APPLIED", "SKIPPED", "FAILED"]

    def update_state(self, job_id, title, company, status, details=""):
        self.data[job_id] = {
            "title": title,
            "company": company,
            "status": status,
            "details": details,
            "updated_at": datetime.utcnow().isoformat()
        }
        with open(APPLIED_FILE, "w") as f:
            json.dump(self.data, f, indent=2)
        print(f"[TRACKER] {job_id} -> {status} ({title} @ {company})")
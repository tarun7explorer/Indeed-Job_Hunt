import os
import json
from dotenv import load_dotenv

load_dotenv()

from browser.browser_manager import BrowserManager, human_delay
from jobs.collector import JobCollector
from jobs.parser import JobParser
from jobs.filter import JobFilter
from ai.nvidia import NVIDIAEngine
from tracking.tracker import Tracker
from notifications.telegram import send_alert
from application.answer_generator import AnswerGenerator
from application.application_handler import ApplicationHandler

def main():
    with open("config/settings.json") as f:
        settings = json.load(f)

    tracker = Tracker()
    job_filter = JobFilter(tracker)
    ai_engine = NVIDIAEngine()
    answer_gen = AnswerGenerator(ai_engine)
    app_handler = ApplicationHandler(answer_gen)

    browser_mgr = BrowserManager(headless=not settings.get("headful", False))
    page = browser_mgr.start()

    collector = JobCollector(page)
    search_queries = collector.build_search_urls(
        target_roles=settings["target_roles"],
        locations=settings["locations"],
        max_age_days=settings.get("max_job_age_days", 3)
    )

    processed_count = 0
    max_jobs = settings.get("max_jobs_per_run", 10)

    for role, loc, search_url in search_queries:
        if processed_count >= max_jobs:
            print(f"[MAIN] Reached max applications limit for this run ({max_jobs}). Stopping.")
            break

        job_cards = collector.fetch_jobs_from_url(search_url)

        for card in job_cards:
            if processed_count >= max_jobs:
                break

            job_id = card.get_attribute("data-jk")
            if not job_filter.should_process(job_id):
                continue

            try:
                card.click()
                human_delay(2, 4)

                title, company = JobParser.extract_details(page)
                tracker.update_state(job_id, title, company, "MATCHED", details=f"Loc: {loc} | Role: {role}")

                success, reason = app_handler.handle(page)
                if success:
                    tracker.update_state(job_id, title, company, "APPLIED")
                    send_alert(
                        f"🚀 *Job Applied Automatically!*\n"
                        f"*Role:* {title}\n"
                        f"*Company:* {company}\n"
                        f"*Location:* {loc}\n"
                        f"*Freshness:* < 3 Days"
                    )
                    processed_count += 1
                else:
                    tracker.update_state(job_id, title, company, "SKIPPED", details=reason)

            except Exception as e:
                tracker.update_state(job_id, "Unknown", "Unknown", "FAILED", details=str(e)[:100])

    browser_mgr.stop()
    print(f"[RUN COMPLETE] Successfully submitted {processed_count} applications across target roles.")

if __name__ == "__main__":
    main()
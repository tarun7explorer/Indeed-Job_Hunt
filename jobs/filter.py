from tracking.tracker import Tracker

class JobFilter:
    def __init__(self, tracker: Tracker):
        self.tracker = tracker

    def should_process(self, job_id):
        if not job_id or self.tracker.is_processed(job_id):
            return False
        return True
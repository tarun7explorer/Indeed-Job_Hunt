import os

class SubmissionChecker:
    @staticmethod
    def can_auto_submit():
        return os.getenv("AUTO_SUBMIT", "true").lower() == "true"
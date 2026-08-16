from browser.selectors import Selectors
from browser.browser_manager import human_delay
from application.answer_generator import AnswerGenerator
from application.submission_checker import SubmissionChecker

class ApplicationHandler:
    def __init__(self, answer_gen: AnswerGenerator):
        self.answer_gen = answer_gen

    def handle(self, page):
        apply_btn = page.locator(Selectors.EASILY_APPLY_BTN)
        if apply_btn.count() == 0 or not apply_btn.first.is_visible():
            return False, "External Link"

        apply_btn.first.click()
        human_delay(3, 5)

        max_steps = 8
        step = 0
        while step < max_steps:
            step += 1
            self.answer_gen.fill_form_fields(page)

            submit_btn = page.locator(Selectors.SUBMIT_BTN)
            continue_btn = page.locator(Selectors.CONTINUE_BTN)

            if submit_btn.count() > 0 and submit_btn.first.is_visible():
                if SubmissionChecker.can_auto_submit():
                    submit_btn.first.click()
                    human_delay(3, 4)
                    return True, "Applied"
                else:
                    return False, "Awaiting Manual Confirmation"

            elif continue_btn.count() > 0 and continue_btn.first.is_visible():
                continue_btn.first.click()
                human_delay(2, 4)
            else:
                return False, "Unsupported Field"

        return False, "Max Steps Exceeded"
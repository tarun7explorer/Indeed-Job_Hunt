from ai.nvidia import NVIDIAEngine
from browser.selectors import Selectors
from browser.browser_manager import human_delay

class AnswerGenerator:
    def __init__(self, ai_engine: NVIDIAEngine):
        self.ai = ai_engine

    def fill_form_fields(self, page):
        # Text fields
        for inp in page.locator(Selectors.TEXT_INPUTS).all():
            if inp.is_visible() and not inp.input_value():
                inp_id = inp.get_attribute("id")
                label = "Screening Question"
                if inp_id and page.locator(f"label[for='{inp_id}']").count() > 0:
                    label = page.locator(f"label[for='{inp_id}']").first.text_content()
                
                ans = self.ai.answer_question(label)
                inp.fill(ans)
                human_delay(1, 2)

        # Dropdowns
        for select in page.locator(Selectors.SELECT_DROPDOWNS).all():
            if select.is_visible():
                opts = [o.text_content().strip() for o in select.locator("option").all() if o.get_attribute("value")]
                if opts:
                    label = select.get_attribute("aria-label") or "Option"
                    chosen = self.ai.answer_question(label, choices=opts)
                    select.select_option(label=chosen)

        # Radio buttons
        for fieldset in page.locator(Selectors.FIELDSETS).all():
            if fieldset.is_visible():
                legend = fieldset.locator("legend").text_content() if fieldset.locator("legend").count() > 0 else "Question"
                labels = fieldset.locator("label").all()
                opts = [l.text_content().strip() for l in labels]
                if opts:
                    chosen = self.ai.answer_question(legend, choices=opts)
                    for label in labels:
                        if chosen.lower() in label.text_content().lower():
                            label.click()
                            break
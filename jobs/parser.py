from browser.selectors import Selectors

class JobParser:
    @staticmethod
    def extract_details(page):
        title_el = page.locator(Selectors.JOB_TITLE)
        comp_el = page.locator(Selectors.COMPANY_NAME)
        
        title = title_el.first.text_content().strip() if title_el.count() > 0 else "Software Development Role"
        company = comp_el.first.text_content().strip() if comp_el.count() > 0 else "Company"
        return title, company
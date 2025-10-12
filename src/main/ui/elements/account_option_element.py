from src.main.ui.elements.base_element import BaseElement


class AccountOption(BaseElement):
    def __init__(self, locator):
        super().__init__(locator)

        self.value = locator.get_attribute("value")
        self.account_number = None
        self.balance = None

        if self.value:  # for the base option there is no data
            self.account_number = locator.inner_text().split()[0]
            self.balance = float(locator.inner_text().split()[2].replace(")", "").replace("$", ""))

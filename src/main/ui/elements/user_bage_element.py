from src.main.ui.elements.base_element import BaseElement


class UserBadgeElement(BaseElement):
    def __init__(self, locator):
        super().__init__(locator)
        self.username, self.role = locator.inner_text().split()

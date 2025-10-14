from abc import ABC


class BaseElement(ABC):
    def __init__(self, locator):
        self.locator = locator

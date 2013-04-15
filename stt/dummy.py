from exceptions import *


class Dummy:
    def __init__(self, text):
        self.text = text

    def get_text(self):
        if not self.text is None:
            return self.text

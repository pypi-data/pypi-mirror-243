import os


class Relative:

    def __init__(self, origin: str = __file__):
        self.origin = origin

    def relative(self, path):
        return os.path.join(os.path.dirname(self.origin), path)


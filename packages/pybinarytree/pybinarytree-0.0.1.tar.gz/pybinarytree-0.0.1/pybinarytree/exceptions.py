
class NotComparableException(Exception):
    def __init__(self):
        super().__init__("Value cannot be compared with objects in tree.")



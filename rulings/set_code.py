from rulings_object import RulingsObject

class Code(RulingsObject):
    """docstring for Code."""
    def __init__(self, code, number):
        self.code = code.lower()
        self.number = str(number)
        self.url = 'cards/{}/{}/rulings'.format(self.code, self.number)
        super(Code, self).__init__(self.url)

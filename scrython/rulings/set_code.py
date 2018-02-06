from .rulings_object import RulingsObject

class Code(RulingsObject):
    def __init__(self, code, collector_number):
        self.code = code.lower()
        self.number = str(collector_number)
        self.url = 'cards/{}/{}/rulings'.format(self.code, self.number)
        super(Code, self).__init__(self.url)

from .rulings_object import RulingsObject

class Code(RulingsObject):
    def __init__(self, code, collector_number):
        self.url = 'cards/{}/{}/rulings?'.format(code.lower(), str(collector_number))
        super(Code, self).__init__(self.url)

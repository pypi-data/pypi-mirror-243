class MElement(object):
    args = {}

    def style(self, sheet: str = None, value: bool = None):
        if value is not None:
            self._args["styles"][sheet] = value
            return self
        else:
            return self._args["styles"][sheet]
        self.update()

    def color(self, sheet: str = None, value: bool = None):
        if value is not None:
            self._args["colors"][sheet] = value
            return self
        else:
            return self._args["colors"][sheet]
        self.update()
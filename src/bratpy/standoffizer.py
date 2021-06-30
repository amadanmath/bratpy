class Standoffizer:
    def __init__(self, text, subs, start=0, skip=False):
        self.text = text
        self.subs = subs
        self.start = start
        self.skip = skip

    def __iter__(self):
        offset = 0
        finder = self.text.find if self.skip else self.text.index
        for sub in self.subs:
            pos = finder(sub, offset)
            if pos != -1:
                offset = pos + len(sub)
                yield (self.start + pos, self.start + offset)
            else:
                yield None

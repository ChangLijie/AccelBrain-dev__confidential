class DotDict(dict):
    def __getattr__(self, name):
        value = self.get(name)
        return DotDict(value) if isinstance(value, dict) else value

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

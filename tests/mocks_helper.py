import copy


class MagicClass(object):
    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            pass

        return wrapper


class MagicClassMaker(object):
    def make_magic(self):
        return copy.deepcopy(MagicClass)


class MethodReplacer(object):
    def return_value(self, value):
        def new_method(*a, **kw):
            return value

        return new_method


import copy

import importlib


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


class MagicClass(object):
    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            pass

        return wrapper


class MagicClassMaker(object):
    def make_magic(self):
        return copy.deepcopy(MagicClass)


class MethodReplacer(object):
    def __init__(self, original_class):
        self.original_class_copy = copy.deepcopy(original_class)
        self.original_class = original_class

    def return_value(self, value):
        def new_method(*a, **kw):
            return value

        return new_method

    def stop(self):
        self.original_class = self.original_class_copy

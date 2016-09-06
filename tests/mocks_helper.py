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
    def __init__(self, class_path):
        self.class_path = class_path

        self.module = self.class_path.rsplit('.', 1)[0]
        self.name = self.class_path.rsplit('.', 1)[1]
        self.class_pristine = copy.deepcopy(class_for_name(self.module, self.name))

    def return_value(self, value):
        def new_method(*a, **kw):
            return value

        return new_method

    def stop(self):
        print self.class_pristine.insert
        setattr(importlib.import_module(self.module), self.name, self.class_pristine)

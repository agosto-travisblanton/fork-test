from google.appengine.api import runtime as profile
from agar.env import on_server

def current_mem(tmpl_str):
    memory = "NOT SUPPORTED"
    if on_server:
        memory = profile.memory_usage().current()
    return tmpl_str.format(memory)
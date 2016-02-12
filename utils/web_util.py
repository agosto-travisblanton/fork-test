from routes import application as default_application
from routes_migration import application as migration_application
from routes_proofplay import application as proofplay_application

MODULE_APPLICATIONS = {
    'migration': migration_application,
    'proofplay': proofplay_application
}


def build_uri(route_name, params_dict={}, module=None):
    application = MODULE_APPLICATIONS.get(module, default_application)
    return application.router.build(None, route_name, None, params_dict)


def is_ascii(s):
    return all(ord(c) < 128 for c in s)

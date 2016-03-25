"""
Functions to initialize environment settings.
"""


def get_project_root():
    """
    Returns the project root path.
    Starts in current working directory and traverses up until app.yaml is found.
    Assumes app.yaml is in project root.
    """
    import os
    start_path = os.path.abspath('.')
    search_path = start_path
    while search_path:
        app_yaml_path = os.path.join(search_path, 'app.yaml')
        if os.path.exists(app_yaml_path):
            break
        search_path, last_dir = os.path.split(search_path)
    else:
        raise os.error('app.yaml not found for env_setup.get_project_root().%sSearch started in: %s' % (os.linesep, start_path))
    return search_path


def setup():
    """Adds <project_root>/lib/substrate and <project_root>/lib/usr to the python path."""
    import os
    import sys
    project_root = get_project_root()
    if os.path.exists(project_root):
        lib_substrate_path = os.path.join(project_root, 'lib', 'substrate')
        if lib_substrate_path not in sys.path:
            sys.path.insert(0, lib_substrate_path)
        lib_usr_path = os.path.join(project_root, 'lib', 'usr')
        if lib_usr_path not in sys.path:
            sys.path.insert(0, lib_usr_path)


def setup_tests():
    """Fix the sys.path to include our extra paths."""
    import os
    import sys

    if not hasattr(sys, 'version_info'):
        sys.stderr.write('Very old versions of Python are not supported. Please '
                         'use version 2.7 or greater.\n')
        sys.exit(1)
    version_tuple = tuple(sys.version_info[:2])
    if version_tuple != (2, 7):
        sys.stderr.write('Warning: Python %d.%d is not supported. Please use '
                         'version 2.7.\n' % version_tuple)

    # Only works for UNIXy style OSes.
    # Find App Engine SDK
    dev_appserver = None
    DIR_PATH = ""

    appengine_sdk_path = os.environ.get('APPENGINE_SDK')
    if appengine_sdk_path:
        dev_appserver_path = os.path.join(appengine_sdk_path, "dev_appserver.py")
        if os.path.isfile(dev_appserver_path):
            sys.path.append(appengine_sdk_path)
            DIR_PATH = appengine_sdk_path
            import dev_appserver
        else:
            sys.stderr.write('WARNING: Could not find dev_appserver.py in APPENGINE_SDK: {}\n'.format(dev_appserver_path))
    else:
        sys.stderr.write('WARNING: Environment variable APPENGINE_SDK not set\n')

    if dev_appserver is None:
        sys.stderr.write('Searching for dev_appserver.py in PATH\n')
        for d in os.environ["PATH"].split(":"):
            dev_appserver_path = os.path.join(d, "dev_appserver.py")
            if os.path.isfile(dev_appserver_path):
                DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(dev_appserver_path)))
                sys.path.append(DIR_PATH)
                import dev_appserver
                sys.path.pop()

    if not DIR_PATH or not dev_appserver:
        sys.stderr.write('Could not find SDK path.  Make sure dev_appserver.py is in your PATH or APPENGINE_SDK\n')
        sys.exit(1)

    if not hasattr(dev_appserver, 'EXTRA_PATHS'):
        sys.stderr.write('dev_appserver module missing attribute EXTRA_PATHS.\n')
        sys.stderr.write('ERROR: dev_appserver is an incompatible version.\n')
        sys.exit(1)

    # Configure path
    extra_paths = dev_appserver.EXTRA_PATHS[:]
    substrate_paths = [
        os.path.join('.', 'lib', 'substrate'),
        os.path.join('.', 'local', 'substrate', 'lib'),
        os.path.join('.', 'local', 'substrate', 'manage'),
    ]
    usr_paths = [
        os.path.join('.', 'lib', 'usr'),
        os.path.join('.', 'local', 'usr', 'lib'),
        os.path.join('.', 'local', 'usr', 'manage'),
    ]
    sys.path = extra_paths + substrate_paths + usr_paths + sys.path
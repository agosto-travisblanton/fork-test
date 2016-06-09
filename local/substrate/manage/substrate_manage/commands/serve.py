""" Run dev_appserver with the correct command-line arguments.
The 'serve' command looks at `snapdeploy.yaml` to figure out which modules need to be served, and then runs
dev_appserver with the correct settings. In addition, a `pre-serve-script` can be specified to run prior to
dev_appserver, to do things such as JS/CSS preprocessing.
"""
import os
import subprocess
import sys
import yaml

CONFIG_FILE = 'snapdeploy.yaml'


def make_default_config():
    return {'module_yaml_files': ['app.yaml']}


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.load(f.read())
    else:
        config = make_default_config()
    if 'module_yaml_files' not in config:
        config['module_yaml_files'] = ['app.yaml']
    return config


def start_server():
    args = []
    if os.path.exists('dispatch.yaml'):
        args += 'dispatch.yaml'
    args = config['module_yaml_files']
    args_to_print = ['dev_appserver.py'] + args + sys.argv[1:]
    if subprocess.call(args_to_print) != 0:
        print "Start server failed; aborting..."
        sys.exit(1)


def pre_serve_script(config):
    if 'pre-serve-script' in config:
        if subprocess.call(config['pre-serve-script'], shell=True) != 0:
            print('Pre-serve script failed; aborting...')
            sys.exit(1)


if __name__ == "__main__":
    config = load_config()
    pre_serve_script(config)
    start_server()

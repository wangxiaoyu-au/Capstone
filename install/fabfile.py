from fabric import task
from fabric import *
from fabric import SerialGroup as Group
from pathlib import Path
import os
from benedict import benedict
from control_lib.collectd import Collectd



def get_local_path(filename, dir='config'):
    return os.path.join(Path(__file__).resolve().parent.parent, dir, filename)


def read_config(filename):
    config_file = get_local_path(filename)
    print("Loading", config_file)
    return benedict.from_yaml(config_file)


def init_modules(config_file):
    config = read_config(config_file)    
    modules = {
        'colletd': Collectd(config),
    }
    return modules

@task
def install(ctx, module, config_file='config.yaml'):
    modules = init_modules(config_file)
    if module in modules:
        modules[module].install()
    else:
        print("Didn't find module {module}".format(module = module))

@task
def start(ctx, module, config_file='config.yaml'):
    modules = init_modules(config_file)
    if module in modules:
        modules[module].start()
    else:
        print("Didn't find module {module}".format(module = module))

@task
def status(ctx, module, config_file='config.yaml'):
    modules = init_modules(config_file)
    if module in modules:
        modules[module].status()
    else:
        print("Didn't find module {module}".format(module = module))
@task
def stop(ctx, module, config_file='config.yaml'):
    modules = init_modules(config_file)
    if module in modules:
        modules[module].stop()
    else:
        print("Didn't find module {module}".format(module = module))

@task
def update(ctx, module, config_file='config.yaml'):
    modules = init_modules(config_file)
    if module in modules:
        modules[module].update()
    else:
        print("Didn't find module {module}".format(module = module))


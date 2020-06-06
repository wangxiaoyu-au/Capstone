from fabric import task
from fabric import *
from fabric import SerialGroup as Group
from pathlib import Path
import os
from benedict import benedict
from control_lib.collectd import Collectd
from control_lib.portforward import Portforward
from control_lib.grafana import Grafana
from control_lib.influxdb import Influxdb
from control_lib.spark import Spark
from control_lib.pip import Pip


def get_local_path(filename, dir='config'):
    return os.path.join(Path(__file__).resolve().parent.parent, dir, filename)


def read_config(filename):
    config_file = get_local_path(filename)
    print("Loading", config_file)
    return benedict.from_yaml(config_file)


def init_modules(config_file):
    config = read_config(config_file)    
    modules = {
        'collectd': Collectd(config),
        'portforward': Portforward(config),
        'grafana': Grafana(config),
        'influxdb': Influxdb(config),
        'spark': Spark(config),
        'pip': Pip(config),
    }
    return modules

def select_modules(module_names, config_file):
    """Select modules with input module names, if no input names, return all modules"""
    all_modules = init_modules(config_file)
    filtered = []
    if module_names == "":
        return all_modules.values()
    for module in module_names.split(','):
        if module in modules:
            filtered.append(module)
        else:
            print("Didn't find module {module}".format(module = module))
    return filtered


@task
def install(ctx, module="", config_file='config.yaml', password=''):
    selected = select_modules(module, config_file)
    for m in selected:
        print("Module name", m.name())
        m.install(password)
        print()


def run_module_action(action, module, config_file):
    selected = select_modules(module, config_file)
    for m in selected:
        print("Run action: {action} in module named {name}".format(action=action, name=m.name())) 
        func = getattr(m, action)
        func()
        print()


@task
def start(ctx, module="", config_file='config.yaml'):
    run_module_action('start', module, config_file)


@task
def status(ctx, module="", config_file='config.yaml'):
    run_module_action('statu', module, config_file)


@task
def stop(ctx, module="", config_file='config.yaml'):
    run_module_action('stop', module, config_file)


@task
def update(ctx, module="", config_file='config.yaml'):
    run_module_action('update', module, config_file)

from fabric.api import env
from fabric.operations import run, put
from fabric.context_managers import cd

env.hosts = ["192.168.1.254"]

def deploy():
    run("mkdir -p /home/fwilson/ircbot")
    put(".", "/home/fwilson/ircbot")

def start():
    with cd("/home/fwilson/ircbot"):
        run("zsh -c 'nohup python run.py &'")

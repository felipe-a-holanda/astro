from fabric.operations import local as lrun, run
from fabric.api import task
from fabric.state import env
from contextlib import contextmanager
from fabric.api import *
 

@task
def local():
    env.run = lrun
    env.activate = '. {directory}/env/bin/activate'.format(**env)
    env.hosts = ['localhost']
    env.directory = '.'
    

@task
def remote():
    env.run = run
    env.hosts = ['root@104.131.231.202']    
    env.directory = '/var/www/astro/'
    env.activate = 'source {directory}/env/bin/activate'.format(**env)
    env.github_repo = 'https://github.com/flp9001/astro.git'
    

@contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


def _install_dependencies():
    with virtualenv():
        env.run("pip install -r {directory}/requirements.txt".format(**env))
    
@task
def deploy():
    with cd(env.directory):
        env.run("git reset --hard")
        env.run("git checkout -f")
    _install_dependencies()
        



@task
def setup():
    env.run('virtualenv env')
    with virtualenv():
        env.run('pip freeze')
    




@task
def install():
    env.run('echo "teste"')

import inspect, os, sys
from fabric.api import task

utils_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), '../utils'))
sys.path.append(utils_path)
import managerutils

@task
def deploy():
	"""
    Perform Full deployment.
    """
	managerutils.deploy()
	return

@task
def restart():
	"""
    Just stop start server
    """
	managerutils.restart()
	return

@task
def cleanrestart():
	"""
    Clean temp files and restart server
    """
	managerutils.cleanrestart()
	return
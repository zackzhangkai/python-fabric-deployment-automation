python-fabric-deployment-automation
===================================

Automated deployment script using Fabric (a Python library), Jenkins

This project does a deployment on the remote server with the archive from the lastSuccessful Jenkins build.


#Assumption:

* This is based on the application 
** using Apache Tomcat as web server
** using Apache as the http server
** Application is hosted on linux environment


#Uses following:

* [Fabric 1.9.0](http://docs.fabfile.org/en/1.9/)
* Paramiko 1.14.0
* Python 2.6.6


#Instructions while working on the code in personal system

* make sure __init__.py is available in the directory to make it a package
* Create your distribution - will also create MANIFEST
** $ cd path/to/Project
** $ python setup.py sdist
* To compile py file
** $ cd path/to/project
** $ python -m py_compile filename.py


#To run the test cases

* $ cd path/to/project/tests
* $ python -m unittest testmanagerutils 


#To run the Fab

* $ cd path/to/project
* $ fab -f bin/manager.py -c settings/{env}/.fabricrc {task_name}
** Example:- fab -f bin/manager.py -c settings/qa/.fabricrc deploy

#Refer the [wiki page on How to Set-up Jenkins for continuous integration](https://github.com/sidnan/python-fabric-deployment-automation/wiki/Setup-for-Git-Jenkins-build-hook)

#Brief Description

To run this project, user must pass a fab file and a settings file (.fabricrc). The fab file holds the tasks. User can list the available [tasks](http://docs.fabfile.org/en/1.9/usage/tasks.html) using the command (** fab -f bin/manager.py -l **). [Settings](http://docs.fabfile.org/en/1.9/usage/fab.html#settings-files) file uses the properties of the remote server (like server name, key, etc.)

[run command](http://docs.fabfile.org/en/1.9/usage/interactivity.html#combining-the-two) **is used to execute the command in the remote machine**.

[disconnect_all command](http://docs.fabfile.org/en/1.9/api/core/network.html#fabric.network.disconnect_all) **is used to disconnect from the remote machine. Invoking run() command again will automatically establish the connection/session.**

[local command](http://docs.fabfile.org/en/1.9/api/core/operations.html#fabric.operations.local) **Run a command on the local system.**



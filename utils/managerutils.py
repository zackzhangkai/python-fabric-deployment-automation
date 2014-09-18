from fabric.operations import run, local
from fabric.state import env
from fabric.network import disconnect_all
import inspect, logging, sys, time, os

#### This managerutils is to invoke the commands separately on the remote machine


#### Initialize variables from env settings file
environment_name = 'None'
path_to_archive = 'None'
max_server_start_cycle = 6
web_app_url = 'None'
try:
        environment_name = env.environment_name
        path_to_archive = env.path_to_archive
        max_server_start_cycle = int(env.max_server_start_cycle)
        web_app_url = env.web_app_url
except AttributeError, e:
        print 'ERROR: Environment variables in the settings file - %s' % str(e)


logs_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), '../logs'))

#### Log level of debug - logs ssh attempts with technicalities
#### Log level of info - just logs the command prints
logging.basicConfig(filename=logs_path+'/App_Name_'+environment_name+'_console.out', format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

### This method takes care of deployment & rollback (if needed)
def deploy():
        try:

                             

                print "INFO: Deploying the Archive from following location: %s " % path_to_archive
                logging.info("Deploying the Archive from following location: %s " % path_to_archive)

				### stop server
				stop()
				
				### remove unwanted files
				clean()
				run('rm -rf $APP_SERVER_DIR/webapps/<archive>', pty=False, combine_stderr=True)
				
				### get the archive from jenkins
				run('wget --progress=bar:force --no-check-certificate -O <$APP_SERVER_DIR/deploy> <http://jenkins/url/to/lastsuccessful/build/archive> ', pty=False, combine_stderr=True)
				
				### start server				
                start()

                

                ### verify
                isDeploymentSuccessful=verify(case='[REGULAR]')

                if isDeploymentSuccessful==True:
                        print 'INFO: Deployment Successful. Invoking backup.'
                        logging.info('Deployment Successful. Invoking backup.')

                        backup()
                else:
                        

                        rollback()

                        isRollBackSuccessful = verify(case='[ROLLBACK]')
                        if isRollBackSuccessful==True:
                                print("ERROR: New build failed. Rolled back.")
                                logging.error('New build failed. Rolled back.')
                        else:
                                print("ERROR: New build failed. Roll back also Failed. Advised to do manual deployment. Later check logs to troubleshoot.")
                                logging.error('New build failed. Roll back also Failed. Advised to do manual deployment. Later check logs to troubleshoot.')
                                raise Exception("Roll back failed!")

        except:
               

                print "ERROR: Aborting Process. Advised to do manual deployment. Later check logs to troubleshoot.", sys.exc_info()[0]
                logging.error("Aborting Process. Advised to do manual deployment. Later check logs to troubleshoot.")
                logging.error(sys.exc_info()[0])
                raise

        print("INFO: End of deployment process.")
        logging.info("End of deployment process.")
        return


### This method verifies is the server and website up
def verify(case=''):
        # verify server start
        # if server up, then verify deployment
        # else, abort
        isServerStarted=verifyserverstartup(case)
        if isServerStarted==True:
                print("INFO: "+case+" Server has been started!")
                logging.info(case+" Server has been started!")

                # verify deployment
                # if success, then update path to back up file
                # else, roll back
                isDeploymentSuccessful=verifydeployment(case)
		return isDeploymentSuccessful
        else:
                print("ERROR: "+case+" Server is not starting. Aborting the Process. Advised to do deployment manually. Later check logs to troubleshoot.")
                logging.error(case+' Server is not starting. Aborting the Process. Advised to do deployment manually. Later check logs to troubleshoot.')
                raise Exception("Server not starting!")
        return

### This method verifies is the website up
def verifydeployment(case=''):
        print("INFO: Waiting for Website to come up.")
        logging.info("Waiting for Website to come up.")
        disconnect_all()
		
		### Sleep for some time till the site is fully up
		### This sleep time can be customized based on needs
        time.sleep(500)

        ### Check is the site is up & running.
        ### If,
        ### return_code=0, site is up
        ### return_code=1, site is down
        ### It takes at most 5mins for my site to come up (otherwise wget will time/error code 3 out). Ping every 60sec.
        result=local('wget --directory-prefix=/tmp/ --delete-after --wait=60 http://'+web_app_url)
        returncode = int(result.return_code)
        print "DEBUG: "+case+" Return code for website verification: %d " % returncode
        logging.debug(case+' Return code for website verification: %d' % returncode)
        isDeploymentSuccessful = (returncode==0)
	return isDeploymentSuccessful
        return

### This method verifies is the server up
def verifyserverstartup(case=''):
        serverCounter=0
        isServerStarted=0
        ### ping every 100s to know has the server started
        while (serverCounter < max_server_start_cycle):
                print 'INFO: '+case+' Waiting for Server to start... %d of %d' % (serverCounter,max_server_start_cycle)
                logging.info(case+' Waiting for Server to start... %d of %d' % (serverCounter,max_server_start_cycle))
                time.sleep(100)
				### run() executes the command in the remote server (which is specified in the settings .fabricrc file)
                isServerStarted=run('grep -c "Server startup in" /path/to/app/server/console.log')
                if int(isServerStarted) > 0:
                        return True
                serverCounter+=1
        return False
        return

### This method backup the archive url which can be used as a roll path for the next deployment
def backup():
        ### Read the build number from the archive manifest, so that it can be used
        ### to get rollback path to archive
        try:
                disconnect_all()
				### Make sure your archive MANIFEST file has the build-number
                manifest_build_line=local('unzip -q -c ' + env.path_to_archive + ' META-INF/MANIFEST.MF | grep Build-Version', capture=True)

                if 'Build-Version' in manifest_build_line:
                        ### Get the build number
                        build_number = manifest_build_line.split()[1]


                        rollback_url = path_to_archive.replace('lastSuccessfulBuild', build_number)

                        ### Update the url in the rollback file
                        with open(env.path_to_rollback, "w") as rollback_log_file:
                                rollback_log_file.write(rollback_url)

                                print 'INFO: Updated roll back log file with url: %s' % rollback_url
                                logging.info('Updated roll back log file with url: %s' % rollback_url)
        except KeyError, e:
                print 'ERROR: %s' % str(e)
                logging.error(str(e))
                raise
        except:
                print "ERROR: while backingup...", sys.exc_info()[0]
                logging.error('while backingup...')
                logging.error(sys.exc_info()[0])
                raise
        return

### This method rollback to the archive logged in the rollback log
def rollback():
        print 'ERROR: New build failed. Rolling back...'
        logging.error('New build failed. Rolling back...')
	
        with open(env.path_to_rollback) as rollback_log_file:
                path_to_archive=rollback_log_file.readline()

        print 'INFO: Rolling back to: %s' % path_to_archive
        logging.info('INFO: Rolling back to: %s' % path_to_archive)

        deploy_app_monitor=run('sudo /opt/JenkinsMgr/bin/deploy_app.sh -i '+environment_name+' -f '+path_to_archive)
        logging.debug(deploy_app_monitor)

        return

def stop():
		### bring down
		print 'Shutting down the server'
		log.info('Shutting down the server')		
                
		monitor_output=run('./path/to/tomcat/bin/shutdown.sh', pty=False, combine_stderr=True)

		logging.debug(monitor_output)
		return


def start():
		### bring up
		print 'Starting the server'
		log.info('Starting the server')
		monitor_output=run('./path/to/tomcat/bin/startup.sh', pty=False, combine_stderr=True)

		logging.debug(monitor_output)
		return	


def restart():
		### bring up
		print 'ReStarting the server'
		log.info('ReStarting the server')
		stop()
		start()
		return

def clean():
		### Clean server
		print 'Clean the server'
		log.info('Clean the server')
		### remove unwanted files
		monitor_output=run('rm -rf $APP_SERVER_DIR/tmp/* $APP_SERVER_DIR/work/*', pty=False, combine_stderr=True)
		
		logging.debug(monitor_output)
		
		return
		
def cleanrestart():
		### bring up
		print 'Clean ReStarting the server'
		log.info('Clean ReStarting the server')
		clean()
		restart()
		return
import paramiko
import json
import boto3
import time

from st2actions.runners.pythonrunner import Action

class StartJavaDebianPackageAction(Action):
    def run(self, instanceid, instanceip, packagename, servicename, key_file_name):

        client = boto3.client('ec2')
        #Ensure instance is in a ready state, call ec2.describe_instance_status and ensure status is 16/running
        code = 0
        maxRetries = 10 #five minutes
        numAttempts = 0
        while ((code != 16) and (numAttempts != maxRetries)):
            reservations = client.describe_instances(InstanceIds=[instanceid])
            for res in reservations["Reservations"]:
                for instance in res["Instances"]:
                    code = instance["State"]["Code"]

            if code != 16:
                numAttempts += 1
                time.sleep(30)

        if((code != 16) and (numAttempts == maxRetries)):
            print("EC2 Instance timed out")

        #Once instance is running wait for port 22 to be activated
        time.sleep(30)

        #Connect to the instance and start app
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(instanceip, username = 'ubuntu', key_filename=key_file_name)
        print "Connected to server."
        dpkgcommand = 'sudo dpkg -i ' + packagename
        stdin, stdout, stderr = ssh.exec_command(dpkgcommand)
        print stdout.readlines()

        startcommand = 'sudo systemctl start ' + servicename
        stdin, stdout, stderr = ssh.exec_command(startcommand)
        ssh.close()

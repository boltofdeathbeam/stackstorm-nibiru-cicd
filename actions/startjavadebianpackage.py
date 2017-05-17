import paramiko
import json
import boto3
import time

from st2actions.runners.pythonrunner import Action

class StartJavaDebianPackageAction(Action):
    def run(self, instanceip, packagename, servicename, key_file_name):

        #Ensure instance is in a ready state, call ec2.describe_instance_status and ensure status is 16/running
        time.sleep(90)

        # Get the instance id
        # with open(instancefile) as data_file:
        #     data = json.load(data_file)

        # instanceId = data["InstanceId"]

        # Get the instance IP address
        # client = boto3.client('ec2')
        #
        # reservations = client.describe_instances(InstanceIds=[instanceid])
        # appIpAddress = ""
        #
        # for res in reservations["Reservations"]:
        #     for instance in res["Instances"]:
        #         appIpAddress = instance["PublicIpAddress"]
        #         break
        #
        # print(appIpAddress)

        #Save ip address to redis

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

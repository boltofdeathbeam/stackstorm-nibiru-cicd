import boto3
import sys
import time

from st2actions.runners.pythonrunner import Action

class CreateEC2InstanceAction(Action):
    def run(self, image_id, security_group_id, instance_type, key_name, app_instance_name):
        ec2 = boto3.resource('ec2')
        client = boto3.client('ec2')

        print('IMAGE ID: ' + image_id)

        instances = ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, SecurityGroupIds=[security_group_id], InstanceType=instance_type, KeyName=key_name)

        appInstanceId = instances[0].id

        appInstanceName = app_instance_name + str(int(round(time.time() * 1000)))

        time.sleep(10)

        response = client.create_tags(Resources=[appInstanceId], Tags=[{ 'Key': 'Name', 'Value': appInstanceName}])

        reservations = client.describe_instances(InstanceIds=[appInstanceId])

        appIpAddress = ""

        for res in reservations["Reservations"]:
            for instance in res["Instances"]:
                appIpAddress = instance["PublicIpAddress"]
                break

        print(appIpAddress)

        instanceMetadata = appInstanceId, appIpAddress

        # file = open('/opt/share/instanceFile.json', 'wb')
        # file.write("{ \n\t\"InstanceId\": \"" + instances[0].id + "\" \n}")
        # file.close

        return (True, instanceMetadata)

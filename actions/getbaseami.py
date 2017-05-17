import boto3
import sys

from st2actions.runners.pythonrunner import Action

class GetAMIAction(Action):
    def run(self, os):
        ec2 = boto3.client('ec2')
        if(os == 'ubuntu1604') :
            amifilter = 'ubuntu1604-lts-pso-autoami-*'
        filters = [{
            'Name': 'name',
            'Values': [amifilter]
        }]

        images = ec2.describe_images(Filters=filters)

        for image in images["Images"] :
            return (True, image["ImageId"])

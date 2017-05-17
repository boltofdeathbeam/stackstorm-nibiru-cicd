import boto3
import sys

from st2actions.runners.pythonrunner import Action

class GetAppAMIAction(Action):
    def run(self, appaminame):
        ec2 = boto3.client('ec2')
        searchstring = appaminame + "-*"
        filters = [{
            'Name': 'name',
            'Values': [searchstring]
        }]

        images = ec2.describe_images(Filters=filters)
        imageNameIdList = []
        for image in images["Images"] :
            t=image["Name"], image["ImageId"]
            imageNameIdList.append(t)

        sortedList = sorted(imageNameIdList, key=lambda imageAttr: imageAttr[0])
        appAmiIdList = sortedList[len(sortedList)-1]
        return (True, appAmiIdList[1])

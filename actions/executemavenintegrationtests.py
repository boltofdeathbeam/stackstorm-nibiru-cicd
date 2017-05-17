import os
import subprocess
import sys

from st2actions.runners.pythonrunner import Action

class ExecuteMavenIntegrationTests(Action):
    def run(self, intscript, instanceip):
        subprocess.call(intscript + ' ' + instanceip, shell=True)

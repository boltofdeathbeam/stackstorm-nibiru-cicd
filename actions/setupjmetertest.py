import sys

from st2actions.runners.pythonrunner import Action

class SetupJMeterTestAction(Action):
    def run(self, instance_ip, jmeter_file):
        tree = et.parse(jmeter_file)
        for element in tree.findall(".//*[@name='HTTPSampler.domain']"):
            print(element.text)
            element.text = instance_ip
            print(element.text)
            tree.write(jmeter_file)

        return (True, jmeter_file)

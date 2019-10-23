import time
import json
import requests


## b23349eb8f7c4f5fb7249f887d448464

## e2314562d1854f9986d5b939d91eda0d

class TrainTime:
    msgStatusCode = 0
    requestCode = 0

    def __init__(self):
        self.update()

    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def update(self):
        response = requests.get('http://api.sl.se/api2/realtimedeparturesV4.json?key=b23349eb8f7c4f5fb7249f887d448464'
        '&siteid=9507'
        '&timewindow=30&Bus=false')
        TrainTime.requestCode = response.status_code

        if TrainTime.requestCode == 200:
            TrainTime.msgStatusCode = response.json()['StatusCode']
            if TrainTime.msgStatusCode == 0:
                ##self.jprint(response.json()['ResponseData']['Trains'])
                self.trains = response.json()['ResponseData']['Trains']
                return True
            else:
                print('TrainTime.msgStatusCode = ' + str(TrainTime.msgStatusCode))
                return False
        else:
            print('TrainTime.response.status_code = ' + str(TrainTime.requestCode))
            return False

    def goingTowardsTCentrum(self):
        output = []
        for index in range(len(self.trains)):
            try:
                if self.trains[index]['JourneyDirection'] == 1:
                    destination = self.trains[index]['Destination']
                    time = self.trains[index]['DisplayTime']
                    output.append(destination + ' ' + time)
            except Exception as e:
                print e.__doc__
                print e.message
        return output

    def comingFromTCentrum(self):
        output = []
        for index in range(len(self.trains)):
            try:
                if self.trains[index]['JourneyDirection'] == 2:
                    destination = self.trains[index]['Destination']
                    time = self.trains[index]['DisplayTime']
                    output.append(destination + ' ' + time)
            except Exception as e:
                print e.__doc__
                print e.message
        return output

#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import urllib2
import xmltodict

class TrainTime:
    def __init__(self):
        self.update()

    def update(self):
        try:
            self.file = urllib2.urlopen(
                'http://api.sl.se/api2/realtimedeparturesV4.xml?key=e2314562d1854f9986d5b939d91eda0d&siteid=9507'
                '&timewindow=30&Bus=false')
            self.data = self.file.read()
            self.file.close()
            self.data = xmltodict.parse(self.data)
            self.trains = self.data['ResponseOfDepartures']['ResponseData']['Trains']['Train']
        except:
            print 'Could not update'
            return False

        return True

    def goingTowardsTCentrum(self):
        output = []
        for index in range(len(self.trains)):
            try:
                if self.trains[index]['JourneyDirection'] == '1':
                    destination = self.trains[index]['Destination']
                    time = self.trains[index]['DisplayTime']
                    output.append(destination + ' ' + time)
                    #print destination + ' ' + time
            except Exception as e:
                print e.__doc__
                print e.message
        return output

    def comingFromTCentrum(self):
        output = []
        for index in range(len(self.trains)):
            try:
                if self.trains[index]['JourneyDirection'] == '2':
                    destination = self.trains[index]['Destination']
                    time = self.trains[index]['DisplayTime']
                    output.append(destination + ' ' + time)
                    #print destination + ' ' + time
            except Exception as e:
                print e.__doc__
                print e.message
        return output

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
        self.trainTime = TrainTime()

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/5x8.bdf")
        textColor = graphics.Color(255, 165, 0)
        pos1 = pos2 = pos3 = pos4 = 0 #offscreen_canvas.width
        my_text = self.args.text
        updateTime = 0
        row1 = "Hello1"
        row2 = "Hello2"
        row3 = "Hello3"
        row4 = "Hello4"

        while True:
            offscreen_canvas.Clear()
            len1 = graphics.DrawText(offscreen_canvas, font, pos1,  7, textColor, row1)
            len2 = graphics.DrawText(offscreen_canvas, font, pos2, 15, textColor, row2)
            len3 = graphics.DrawText(offscreen_canvas, font, pos3, 23, textColor, row3)
            len4 = graphics.DrawText(offscreen_canvas, font, pos4, 31, textColor, row4)
            pos2 -= 1
            pos4 -= 1
            if (pos1 + len1 < 0):
                pos1 = offscreen_canvas.width
            if (pos2 + len2 < 0):
                pos2 = offscreen_canvas.width
            if (pos3 + len3 < 0):
                pos3 = offscreen_canvas.width
            if (pos4 + len4 < 0):
                pos4 = offscreen_canvas.width
            time.sleep(0.04)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            
            currentTime = time.time()
            if (currentTime - updateTime >= 60):
                updateTime = currentTime
                success = self.trainTime.update()
                if success:
                    row1 = "No trains to Centrum"
                    row2 = ""
                    row3 = "No trains from Centrum"
                    row4 = ""
                    toCentrum = self.trainTime.goingTowardsTCentrum()
                    if len(toCentrum) > 0:
                        row1 = toCentrum[0]
                        for i in range(1, len(toCentrum)):
                            row2 += toCentrum[i] + "     "
                    fromCentrum = self.trainTime.comingFromTCentrum()
                    if len(fromCentrum) > 0:
                        row3 = fromCentrum[0]
                        for i in range(1, len(fromCentrum)):
                            row4 += fromCentrum[i] + "     "
                else:
                    row1 = row2 = row3 = row4 = "";
                    row2 = "Error in communication with SL."
                    row4 = "(-.-) Zzz..."
                    

##    def GoingTowardsTCentrumDestintion(self):
##        self.data = self.file.read()
##        self.file.close()
##        self.data = xmltodict.parse(self.data)
##        self.data1 = self.data['ResponseOfDepartures']['ResponseData']['Trains']['Train']
##        text = []
##        for index in range(len(self.data1)):
##            if self.data1[index]['JourneyDirection'] == '2':
##                self.destination = self.data1[index]['Destination']
##
##    def ComingFromTCentrum(self):
##        self.data = self.file.read()
##        self.file.close()
##        self.data = xmltodict.parse(self.data)
##        self.data = self.data['ResponseOfDepartures']['ResponseData']['Trains']['Train']
##        for index in range(len(self.data)):
##            if self.data[index]['JourneyDirection'] == '1':
##                print self.data[index]['Destination']

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()



#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import urllib2
import xmltodict


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
	self.file = urllib2.urlopen(
            'http://api.sl.se/api2/realtimedeparturesV4.xml?key=e2314562d1854f9986d5b939d91eda0d&siteid=9507'
            '&timewindow=30&Bus=false')

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("fonts/5x8.bdf")
        textColor = graphics.Color(124, 255, 125)
        pos1 = pos2 = pos3 = pos4 = 0 #offscreen_canvas.width
        my_text = self.args.text



        while True:
            offscreen_canvas.Clear()
            len1 = graphics.DrawText(offscreen_canvas, font, pos1,  7, textColor, "Stockholm C     5min")
            len2 = graphics.DrawText(offscreen_canvas, font, pos2, 15, textColor, "Tumba 8min * Sodertalje 12min")
            len3 = graphics.DrawText(offscreen_canvas, font, pos3, 23, textColor, "Marsta   3min")
            len4 = graphics.DrawText(offscreen_canvas, font, pos4, 31, textColor, "Uppsala C 7min * Upplands Vasby 11min (hem till Sebbe)")
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
            time.sleep(0.00)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def GoingTowardsTCentrumDestintion(self):
        self.data = self.file.read()
        self.file.close()
        self.data = xmltodict.parse(self.data)
        self.data1 = self.data['ResponseOfDepartures']['ResponseData']['Trains']['Train']
        text = []
        for index in range(len(self.data1)):
            if self.data1[index]['JourneyDirection'] == '2':
                self.destination = self.data1[index]['Destination']

    def ComingFromTCentrum(self):
        self.data = self.file.read()
        self.file.close()
        self.data = xmltodict.parse(self.data)
        self.data = self.data['ResponseOfDepartures']['ResponseData']['Trains']['Train']
        for index in range(len(self.data)):
            if self.data[index]['JourneyDirection'] == '1':
                print self.data[index]['Destination']

# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()



#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
from trainTimeParser import TrainTime
import time


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


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()

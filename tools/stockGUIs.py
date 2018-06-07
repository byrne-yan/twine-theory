import pyqtgraph as pg
import numpy as np

STICK_OPTIONS = {
    'width':2,
    'gap':1,
    'color':'r',
    'fillColor':'r',
    'lineWidth': 1 #px
}

class StickWidget():
    def __init__(self,plot,kSeries,fill=False):
        self.baseX = 0        
        coords = np.array([]).reshape(0,2)
        baseX = 0
        for k in kSeries:
            stick = self.mkStick(k.low,k.high,fill)
            for p in stick: plot.addItem(p)

##        import pdb; pdb.set_trace()

    def mkStick(self,low,high,fill=False):
        p = pg.mkPen(STICK_OPTIONS['color'],width=STICK_OPTIONS['lineWidth'])
        b = pg.mkBrush(STICK_OPTIONS['fillColor'])

        lx = self.baseX + STICK_OPTIONS['gap']
        rx = self.baseX + STICK_OPTIONS['gap']+STICK_OPTIONS['width']
        self.baseX += STICK_OPTIONS['gap']+STICK_OPTIONS['width']

        if fill:
            lb = pg.PlotCurveItem(x=[lx,lx,rx], y=[high,low,low], pen = p ) #leff-bottom half
            rt = pg.PlotCurveItem(x=[lx,rx,rx], y=[high,high,low], pen =p ) #right-top half
            fill = pg.FillBetweenItem(lb,rt,brush=b, pen = p)           
            return [lb,rt,fill]
        else:
            stick = pg.PlotCurveItem(x= [lx,lx,rx,rx,lx], y = [high,low,low,high,high], pen = p)
            return [stick]

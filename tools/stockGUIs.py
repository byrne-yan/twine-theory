import pyqtgraph as pg
import numpy as np

STICK_OPTIONS = {
    'width':2,
    'gap':1,
    'color':'r',
    'fillColor':'b',
    'lineWidth': 1 #px
}

class StickWidget():
    def __init__(self,plot,kSeries):
        self.baseX = 0        
        coords = np.array([]).reshape(0,2)
        baseX = 0
        conn = []
        for k in kSeries:
            coords = np.concatenate((coords,self.mkStick(k.low,k.high)))
            conn +=[True,True,True,True,False]

        p = pg.mkPen(STICK_OPTIONS['color'],width=STICK_OPTIONS['lineWidth'])
        b = pg.mkBrush(STICK_OPTIONS['fillColor'])
##        import pdb; pdb.set_trace()
        
        stick = plot.addItem(pg.PlotDataItem(coords,pen=p
##                                             ,fillLevel=1.0, fillBrush = pg.mkBrush(STICK_OPTIONS['fillColor'])
                                             ,connect = 'finite'
                                             ))

    def mkStick(self,low,high):
        baseX = self.baseX + STICK_OPTIONS['gap']
        coord = np.array([[float('nan'),float('nan')],[baseX,low],[baseX,high],[baseX+STICK_OPTIONS['width'],high],[baseX+STICK_OPTIONS['width'],low],[baseX,low]])
        self.baseX += STICK_OPTIONS['gap']+STICK_OPTIONS['width']
        return coord

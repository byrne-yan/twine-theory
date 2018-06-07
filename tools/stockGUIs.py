import pyqtgraph as pg
import numpy as np

DEFAULT = {
    'gap':1,
    'width':2,
    'color':'r',
    'fillColor':'g',
    'lineWidth': 1 #px
}
class StickWidget():
    def __init__(self,plot,kSeries,style=DEFAULT):
        self.style = style
        self.baseX = 0        
        coords = np.array([]).reshape(0,2)
        baseX = 0
        for k in kSeries:
            stick = self.mkStick(k.low,k.high,k.start,k.end)
            for p in stick: plot.addItem(p)

##        import pdb; pdb.set_trace()

    def mkStick(self,low,high,start,end):
        goingup = False
        if start < end:
            goingup = True
            p = pg.mkPen(self.style['color'],width=self.style['lineWidth'])
        else:
            p = pg.mkPen(self.style['fillColor'],width=self.style['lineWidth'])
            b = pg.mkBrush(self.style['fillColor'])           
        

        lx = self.baseX + self.style['gap']
        mx = self.baseX + self.style['gap'] + self.style['width']/2
        rx = self.baseX + self.style['gap'] + self.style['width']
        self.baseX += self.style['gap'] + self.style['width']

        if goingup == False:
            lb = pg.PlotCurveItem(x=[mx,mx,lx,lx,mx], y=[high,start,start,end,end], pen = p ) #leff-bottom half
            rt = pg.PlotCurveItem(x=[mx,mx,rx,rx,mx], y=[low,end,end,start,start], pen =p ) #right-top half
            fill = pg.FillBetweenItem(lb,rt,brush=b, pen = p)           
            return [lb,rt,fill]
        else:
            stick = pg.PlotCurveItem(x=  [mx,  mx,  lx,  lx,   mx, mx,   mx,   rx, rx, mx],
                                     y = [high,end, end, start,start,low,start,start,end,end], pen = p)
            return [stick]

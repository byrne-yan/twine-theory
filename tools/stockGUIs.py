import pyqtgraph as pg
import numpy as np

DEFAULT = {
    'gap':1,
    'width':2,
    'color':'r',
    'fillColor':(0,100,0),
    'lineWidth': 1 #px
}

class StickXAxisItem(pg.AxisItem):
    def __init__(self,orientation, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super().__init__(orientation, pen, linkView, parent, maxTickLength, showValues)
        self.dates = []
        
    def setDates(self,dates,span):
        self.span = span
        self.dates = dates;
##    def setTicks(self, ticks):
##        print("##",ticks)
##        super().setTicks(ticks)

##    def tickSpacing(self, minVal, maxVal, size):
##        print("@@",minVal, maxVal, size)
##        if minVal <0 :
##            minVal = 0
##            size += minVal
##        levels = super().tickSpacing(0, maxVal, size)
##        print("@@",levels)
##        return levels

    def tickValues(self, minVal, maxVal, size):
        if minVal <0 :
            minVal = 0
            size += minVal
        values = super().tickValues(minVal, maxVal, size)
##        print(values)
        return  values
         
    def tickStrings(self, values, scale, spacing):

        if self.logMode:
            return self.logTickStrings(values, scale, spacing)
        
        strings = []
        for v in values:
            vs = int(v * scale/self.span)
            
            if vs >= 0 and vs < len(self.dates):                
                strings.append("{}".format(self.dates[vs]))
##        print("$$",values,strings)
        return strings
    
class StickWidget(pg.PlotItem):
    def __init__(self,kSeries,style=DEFAULT):
        self.dateAxis = StickXAxisItem('bottom')
        super().__init__(axisItems={'bottom':self.dateAxis})
        self.style = style
        self.baseX = 0        
        coords = np.array([]).reshape(0,2)
        baseX = 0
        dates = []
        for k in kSeries:
            dates.append(k.time)
            stick = self.mkStick(k.low,k.high,k.start,k.end)
            for p in stick: self.addItem(p)
        
        self.dateAxis.setDates(dates,self.style['gap'] + self.style['width'])

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

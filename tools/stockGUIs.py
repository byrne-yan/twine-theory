import pyqtgraph as pg
import numpy as np

DEFAULT = {
    'gap': 1,
    'width': 2,
    'color': 'r',
    'fillColor': (0, 100, 0),
    'mergedColor': 'g',
    'lineWidth': 1,  # px
    'biColor':'b',
    'segmentColor':'r',
    'showStick':True,
    'showMerge':True,
    'showStroke':True,
    'showSegment':True,
    'showTwine':True
}

class StickXAxisItem(pg.AxisItem):
    def __init__(self, orientation, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super().__init__(orientation, pen, linkView, parent, maxTickLength, showValues)
        self.dates = []

    def setDates(self, dates, span):
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
        if minVal < 0:
            minVal = 0
            size += minVal
        values = super().tickValues(minVal, maxVal, size)
        ##        print(values)
        return values

    def tickStrings(self, values, scale, spacing):

        if self.logMode:
            return self.logTickStrings(values, scale, spacing)

        strings = []
        for v in values:
            vs = int(v * scale / self.span)

            if vs >= 0 and vs < len(self.dates):
                strings.append("{}".format(self.dates[vs]))
        ##        print("$$",values,strings)
        return strings


class StickWidget(pg.PlotItem):
    def __init__(self, kseq, style=DEFAULT):
        print("Construting Widget...")
        self.dateAxis = StickXAxisItem('bottom')
        super().__init__(axisItems={'bottom': self.dateAxis})
        self.style = style
        dates = []
        if True:
            self.baseX = 0
            coords = np.array([]).reshape(0, 2)
            mergedFound = -1
            baseX = 0
            for i in range(0, len(kseq.getSeq())):
                k = kseq.getSeq()[i]
                dates.append(k.time)

                if self.style['showStick']:
                    stick = self.mkStick(k.low, k.high, k.start, k.end)
                    for p in stick: self.addItem(p)

                if self.style['showMerge']:
                    if mergedFound != -1:
                        m = kseq.getSeq()[mergedFound].merged
                        if k.merged != m:
                            stick = self.mkMergedStick(m.low, m.high, mergedFound * (self.style['gap'] + self.style['width']),
                                                       mergedFound, i)
                            for p in stick: self.addItem(p)

                        if not k.merged:
                            mergedFound = -1
                        elif k.merged != m:
                            mergedFound = i
                            baseX = self.baseX

                    elif k.merged:
                        mergedFound = i
                        baseX = self.baseX

        if self.style['showStroke']:
            for p in self.mkStrokeCurve(kseq):
                self.addItem(p)

        if self.style['showSegment']:
            for p in self.mkSegmentCurve(kseq):
                self.addItem(p)
            
        self.dateAxis.setDates(dates, self.style['gap'] + self.style['width'])

    def mkStick(self, low, high, start, end):
        goingup = False
        if start < end:
            goingup = True
            p = pg.mkPen(self.style['color'], width=self.style['lineWidth'])
        else:
            p = pg.mkPen(self.style['fillColor'], width=self.style['lineWidth'])
            b = pg.mkBrush(self.style['fillColor'])

        lx = self.baseX + self.style['gap']
        mx = self.baseX + self.style['gap'] + self.style['width'] / 2
        rx = self.baseX + self.style['gap'] + self.style['width']
        self.baseX += self.style['gap'] + self.style['width']

        if goingup == False:
            lb = pg.PlotCurveItem(x=[mx, mx, lx, lx, mx], y=[high, start, start, end, end], pen=p)  # leff-bottom half
            rt = pg.PlotCurveItem(x=[mx, mx, rx, rx, mx], y=[low, end, end, start, start], pen=p)  # right-top half
            fill = pg.FillBetweenItem(lb, rt, brush=b, pen=p)
            return [lb, rt, fill]
        else:
            stick = pg.PlotCurveItem(x=[mx, mx, lx, lx, mx, mx, mx, rx, rx, mx],
                                     y=[high, end, end, start, start, low, start, start, end, end], pen=p)
            return [stick]

    def mkMergedStick(self, low, high, baseX, idxFrom, idxTo):
        p = pg.mkPen(self.style['mergedColor'], width=self.style['lineWidth'] * 2, style=pg.QtCore.Qt.DashLine)

        lx = baseX + self.style['gap']
        rx = baseX + (self.style['gap'] + self.style['width']) * (idxTo - idxFrom)

        stick = pg.PlotCurveItem(x=[lx, rx, rx, lx, lx],
                                 y=[high, high, low, low, high], pen=p)
        return [stick]

    def mkStrokeCurve(self,kseq):
        #import pdb;pdb.set_trace()
        p = pg.mkPen(self.style['biColor'], width=self.style['lineWidth'])
        p2 = pg.mkPen(self.style['biColor'], width=self.style['lineWidth'], style=pg.QtCore.Qt.DashLine)

        x = [kseq._strokes[0]['from'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2]
        y = [kseq._strokes[0]['from'][1]]
        for i in range(0,len(kseq._strokes)-1):
            x.append(kseq._strokes[i]['to'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2)
            y.append(kseq._strokes[i]['to'][1])

        if kseq._strokes[-1]['growing']:
            if 1==len(kseq._strokes):
                x2 = [kseq._strokes[-1]['from'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2,
                      kseq._strokes[-1]['to'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2]
                y2 = [kseq._strokes[-1]['from'][1],kseq._strokes[-1]['to'][1]]
                return [pg.PlotCurveItem(x2, y2, pen=p2)]
            else:
                x2 = [kseq._strokes[-2]['to'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2,
                      kseq._strokes[-1]['to'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2]
                y2 = [kseq._strokes[-2]['to'][1],kseq._strokes[-1]['to'][1]]
                return [pg.PlotCurveItem(x, y, pen=p),pg.PlotCurveItem(x2, y2, pen=p2)]
        else:
            return [pg.PlotCurveItem(x, y, pen=p)]

    def mkSegmentCurve(self,kseq):
        if kseq._segment and len(kseq._segment):
            p1 = pg.mkPen(self.style['segmentColor'], width=self.style['lineWidth'])
            p2 = pg.mkPen(self.style['segmentColor'], width=self.style['lineWidth'], style=pg.QtCore.Qt.DashLine)

            x = [kseq._segment[0]['from'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2]
            y = [kseq._segment[0]['from'][1]]
            for i in range(0,len(kseq._segment)-1):
                x.append(kseq._segment[i]['to'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2)
                y.append(kseq._segment[i]['to'][1])
            if kseq._segment[-1]['growing']:
                if 1 == len(kseq._segment):
                    x2 = [kseq._segment[-1]['from'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2,
                          kseq._segment[-1]['to'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2]
                    y2 = [kseq._segment[-1]['from'][1],kseq._segment[-1]['to'][1]]
                    return [pg.PlotCurveItem(x2, y2, pen=p2)]
                else:
                    x2 = [kseq._segment[-2]['to'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2,
                          kseq._segment[-1]['to'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2]
                    y2 = [kseq._segment[-2]['to'][1],kseq._segment[-1]['to'][1]]
                    return [pg.PlotCurveItem(x, y, pen=p1),pg.PlotCurveItem(x2, y2, pen=p2)]
            else:
                x.append(kseq._segment[-1]['to'][0]*(self.style['gap']+self.style['width'])+self.style['gap']+self.style['width']/2)
                y.append(kseq._segment[-1]['to'][1])
                
           
            return [pg.PlotCurveItem(x, y, pen=p1)]
        return []

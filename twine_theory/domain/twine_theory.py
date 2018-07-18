import pandas as pd
import sys
from . import segments
from . import strokes

class K:
    def __init__(self, time, startPrice, highPrice, endPrice, lowPrice, volume, level=1):
        self.level = level
        self.time = time
        self.volume = volume
        self.start = startPrice
        self.end = endPrice
        self.low = lowPrice
        self.high = highPrice

    def __getattr__(self, attr):
        if attr == 'top':
            return self.high
        elif attr == 'bottom':
            return self.low
    def __getitem__(self,index):
        if index == 'high':
            return self.high
        elif index == 'low':
            return self.low
        elif index == 'time':
            return self.time

    def __str__(self):
        return "{date:%s,open:%f,close:%f,high:%f,low:%f}" % (self.time,self.start,self.end,self.high,self.low)

    def __repr__(self):
        return str(self)

def kseq_dir(k1, k2):
    if k1.low < k2.low and k1.high < k2.high:
        return 'up'
    elif k1.low > k2.low and k1.high > k2.high:
        return 'down'
    return 'inclusion'


def kseq_merge(k1, k2, isUp):
    if isUp:
        return K(k2.time, k1.start, max(k1.high, k2.high), k2.end, max(k1.low, k2.low), k1.volume + k2.volume)
    return K(k2.time, k1.start, min(k1.high, k2.high), k2.end, min(k1.low, k2.low), k1.volume + k2.volume)


class KSeq:
    def __init__(self, level, klist):
        self._level = level

        if type(klist) is not list and type(klist) is not pd.DataFrame:
            raise TypeError()
        if type(klist) is list and len(klist) > 0 and (type(klist[0]) is not dict) \
            and (type(klist[0]) is not K) and (type(klist[0]) is not tuple):
            raise TypeError()

        self._seq = []
        if type(klist) is pd.DataFrame:
            for i,row in klist.iterrows():
##                import pdb;pdb.set_trace()
                self._seq.append(K(row.name, row['open'], row['high'], row['close'], row['low'], row['volume']))
        else:
            if len(klist) > 0 and type(klist[0]) is dict:
                for k in klist:
                    self._seq.append(K(k['time'], k['start'], k['high'], k['end'], k['low'], k['volume']))

            if len(klist) > 0 and type(klist[0]) is tuple:
                for k in klist:
                    self._seq.append(K(k[0], k[1], k[2], k[3], k[4], k[5]))

        self._low = float('+inf')
        self._high = float('-inf')
        for k in self._seq:
            if k.low < self._low: self._low = k.low
            if k.high > self._high: self._high = k.high
        self._norm = []
        if len(self._seq):
            print("Normalizing...",end='')
            self._normalize()
            print("OK")
            
        print("Resolving strokes...",end='')
        self.split_strokes()
        print("OK")
        
        print("Resolving segments...",end='')
        self.makeupSegment()
        print("OK")

        #import pdb;pdb.set_trace()

    def addK(self, k):
        self._seq.append(k)
        if k.low < self._low: self._low = k.low
        if k.high > self._high: self._high = k.high
        # adjust last kseq_type

    def getDuration(self):
        return {'from': self._seq[0], 'to': self._seq[-1]}

    def __getattr__(self, attr):
        if attr == 'top':
            return self._high
        elif attr == 'bottom':
            return self._low

    def _normalize(self):
        self._norm = [self._seq[0]]
        direction = 'up'
        for i in range(1, len(self._seq)):
            ndir = kseq_dir(self._norm[-1], self._seq[i])
            if ndir == 'inclusion':
                prev = self._norm[-1]
                nk = kseq_merge(prev, self._seq[i], direction == 'up')
                self._seq[i].merged = nk
                if not prev.merged: prev.merged = nk

                nk.merged = True
                if self._norm[-1].ingredient:
                    nk.ingredient = self._norm[-1].ingredient + [i]
                else:
                    nk.ingredient = [i - 1, i]

                j = i - 1
                while j >= 0 and self._seq[j].merged == self._norm[-1]:
                    self._seq[j].merged = nk
                    j -= 1

                self._norm[-1] = nk

            else:
                self._norm.append(self._seq[i])
                direction = ndir

    def getSeq(self):
        return self._seq

    def getNorm(self):
        return self._norm

    def _nextTop(self,start):
        if start + 4 >= len(self._norm):
            return None
        i = start
        while i + 4 < len(self._norm):
            if 'top' == kseq_type(self._norm[i-1],self._norm[i],self._norm[i+1])\
                and 'down' == kseq_type(self._norm[i+2],self._norm[i+3],self._norm[i+4]):
                return i
            i += 1

    def _nextBottom(self,start):
        if start + 4 >= len(self._norm):
            return None
        i = start
        while i + 4 < len(self._norm):
            if 'bottom' == kseq_type(self._norm[i-1],self._norm[i],self._norm[i+1])\
                and 'up' == kseq_type(self._norm[i+2],self._norm[i+3],self._norm[i+4]):
                return i
            i += 1

    def getRealLowestK(self,n):
        assert self._norm[n].merged
        for i in self._norm[n].ingredient:
            if abs(self._seq[i].low - self._norm[n].low) < 0.00000001:
                return i

    def getRealHighestK(self,n):
        assert self._norm[n].merged
        for i in self._norm[n].ingredient:
            if abs(self._norm[n].high - self._seq[i].high) < 0.00000001:
                return i

    def look4LastMerged(self,n):
        for i in range(n,0,-1):
            if self._norm[i].merged:
                return i
        return None
    def split_strokes(self):
        self._strokes = []
        strokes.resolve_strokes(self._norm,0,len(self._norm),self._strokes)
        #map index in _norm into index in _seq
        
        for i in range(0,len(self._strokes)):
##            import pdb;pdb.set_trace()
            b = self._strokes[i]

            
            if self._norm[b['to'][0]].merged:
                if b['isUp']:
                    end = self.getRealHighestK(b['to'][0])
                else:
                    end = self.getRealLowestK(b['to'][0])
            else:
                end = b['to'][0]
                last = self.look4LastMerged(b['to'][0])
                if last:
                    delta = b['to'][0] - last                        
                    end = self._norm[last].ingredient[-1] + delta

            if i ==0:
                start = b['from'][0]
                if self._norm[b['from'][0]].merged : #
                    if b['isUp']:
                        start = self.getRealLowestK(b['from'][0])
                    else:
                        start = self.getRealHighestK(b['from'][0])
                    
            else:
                start = self._strokes[i-1]['to'][0]

            b.changeIndex(self._seq,start,end+1)
                
        
##    def split_strokes2(self):
##        self._strokes = []
##
##        if self._norm and len(self._norm) >= 2:
##            #looking for first 'up' or down k sequence
##            i = 2
##            while i < len(self._norm):
##                t = kseq_type(self._norm[i-2],self._norm[i-1],self._norm[i])
##                if t == 'up': #found up k seq
##                    #looking for lowest K backward
##                    lowest = (i-2, self._norm[i-2].low)
##                    for j in range(i-3, 0, -1):
##                        if self._norm[j].low < lowest[1]:
##                            lowest = (j, self._norm[j].low)
##                    self._strokes.append({
##                        'from': lowest,
##                        'to': (i, self._norm[i].high),
##                        'isUp': True,
##                        'growing': True
##                    })
##                    break
##                elif t == 'down':
##                    #looking for highest K backward
##                    highest = (i-2, self._norm[i-2].high)
##                    for j in range(i-3, 0, -1):
##                        if self._norm[j].high > highest[1]:
##                            highest = (j, self._norm[j].high)
##                    self._strokes.append({
##                        'from': highest,
##                        'to': (i, self._norm[i].low),
##                        'isUp': False,
##                        'growing': True
##                    })
##                    break
##                else:
##                    i += 1
##            #import pdb; pdb.set_trace()
##            while i+2 < len(self._norm):                
##                t = kseq_type(self._norm[i],self._norm[i+1],self._norm[i+2])
##                if self._strokes[-1]['isUp']:
##                    #import pdb; pdb.set_trace()
##                    
##                    if t == 'top' and self._norm[i+1].high >= self._strokes[-1]['to'][1]:
##                        self._strokes[-1]['to'] = (i+1,self._norm[i+1].high)
##                    elif t == 'bottom' and i+1- self._bi[-1]['to'][0] > 3:
##                        self._bi[-1]['growing'] = False
##                        self._bi.append({
##                            'from': self._bi[-1]['to'],
##                            'to': (i+1, self._norm[i+1].low),
##                            'isUp': False,
##                            'growing': True
##                        })
##                else:                    
##                    #import pdb; pdb.set_trace()
##                    if t == 'bottom' and self._norm[i+1].low <= self._bi[-1]['to'][1]:
##                        self._bi[-1]['to'] = (i+1,self._norm[i+1].low)
##                    elif t == 'top' and i+1- self._bi[-1]['to'][0] > 3:
##                        #import pdb; pdb.set_trace()
##                        self._bi[-1]['growing'] = False
##                        self._bi.append({
##                            'from': self._bi[-1]['to'],
##                            'to': (i+1, self._norm[i+1].high),
##                            'isUp': True,
##                            'growing': True
##                        })
##                i = i + 1
##
##            #map index in _norm into index in _seq
##            for i in range(0,len(self._bi)):
##                b = self._bi[i]
##                if i ==0:
##                    if self._norm[b['from'][0]].merged : #
##                        if b['isUp']:
##                            b['from'] = (self.getRealLowestK(b['from'][0]),b['from'][1])
##                        else:
##                            b['from'] = (self.getRealHighestK(b['from'][0]),b['from'][1])
##                        
##                else:
##                    b['from'] = self._bi[i-1]['to']
##                    
##                if self._norm[b['to'][0]].merged:
##                    if b['isUp']:
##                        b['to'] = (self.getRealHighestK(b['to'][0]),b['to'][1])
##                    else:
##                        b['to'] = (self.getRealLowestK(b['to'][0]),b['to'][1])
##                else:
##                    last = self.look4LastMerged(b['to'][0])
##                    if last:
##                        delta = b['to'][0] - last                        
##                        b['to'] = (self._norm[last].ingredient[-1] + delta, b['to'][1])
    def makeupSegment(self):
        self._segment = []
        segments.resolveSeg(self._strokes,0,len(self._strokes),self._segment)
        
   
def kseq_type(k1, k2, k3):
    if k1.low <= k2.low and k1.high <= k2.high and \
        k2.low <= k3.low and k2.high <= k3.high:
        return 'up'
    elif k1.low >= k2.low and k1.high >= k2.high and \
        k2.low >= k3.low and k2.high >= k3.high:
        return 'down'
    elif k1.low < k2.low and k1.high < k2.high and \
        k2.low > k3.low and k2.high > k3.high:
        return 'top'
    elif k1.low > k2.low and k1.high > k2.high and \
        k2.low < k3.low and k2.high < k3.high:
        return 'bottom'
    return 'unnormalized'


class Twine:
    def __init__(self, t1, t2, t3, name='A'):
        self.trends = [t1, t2, t3]
        self.name = name

    def __getattr__(self, attr):

        if attr == 'zg':
            val = 0
            for t in self.trends: val = min(val, t.top)
            return val
        elif attr == 'zd':
            val = sys.maxszie
            for t in self.trends: val = max(val, t.bottom)
            return val
        elif attr == 'dd':
            val = 0
            for t in self.trends: val = max(val, t.top)
            return val
        elif attr == 'dd':
            val = sys.maxszie
            for t in self.trends: val = min(val, t.bottom)
            return val


class Trend:
    def __init__(self, *subtrends):
        self.subtrends = subtrends

    def __getattr__(self, attr):
        if attr == 'top':
            val = 0
            for t in self.subtrends: val = max(val, t.top)
            return val
        elif attr == 'bottom':
            val = sys.maxsize
            for t in self.subtrends: val = min(val, t.bottom)
            return val
        elif attr == 'perfect':
            return


class CongestedTrend(Trend):
    pass


class StrongTrend(Trend):
    pass


class OverflowUp:
    pass


class OverflowDown:
    pass



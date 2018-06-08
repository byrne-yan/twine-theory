import sys

class Twine:
    def __init__(self,t1,t2,t3,name='A'):
        self.trends = [t1,t2,t3]
        self.name = name

    def __getattr__(self,attr):
        
        if attr=='zg':
            val = 0
            for t in self.trends: val = min(val, t.top)
            return val
        elif attr=='zd':
            val = sys.maxszie
            for t in self.trends: val = max(val, t.bottom)
            return val
        elif attr=='dd':
            val = 0
            for t in self.trends: val = max(val, t.top)
            return val
        elif attr=='dd':
            val = sys.maxszie
            for t in self.trends: val = min(val, t.bottom)
            return val

class Trend:
    def __init__(self,*subtrends):
        self.subtrends = subtrends
        
    def __getattr__(self,attr):
        if attr=='top':
            val = 0
            for t in self.subtrends: val = max(val, t.top)
            return val
        elif attr=='bottom':
            val = sys.maxsize
            for t in self.subtrends: val = min(val, t.bottom)
            return val
        elif attr=='perfect':
            return 
class CongestedTrend(Trend):
    pass

class StrongTrend(Trend):
    pass

class OverflowUp:
    pass

class OverflowDown:
    pass

class Bi:
    def __init__(self):
        pass
        

class K:
    def __init__(self, time, startPrice,highPrice, endPrice, lowPrice, volume, level=1):
        self.level = level
        self.time = time
        self.volume = volume
        self.start = startPrice
        self.end = endPrice
        self.low = lowPrice
        self.high = highPrice

    def __getattr__(self,attr):
        if attr=='top': return self.high
        elif attr=='bottom': return self.low

    def __str__(self):
        return '"time":"'+self.time+'","low":'+str(self.low)+',"high":'+str(self.high)+',"start":'+str(self.start)+',"end":'+str(self.end)+',"volume":'+str(self.volume)

    
   
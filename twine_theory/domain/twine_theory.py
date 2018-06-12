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

##    def __str__(self):
##        return '"time":"'+self.time+'","low":'+str(self.low)+',"high":'+str(self.high)+',"start":'+str(self.start)+',"end":'+str(self.end)+',"volume":'+str(self.volume)

def kseq_dir(k1,k2):
    if k1.low < k2.low and k1.high < k2.high: return 'up'
    elif k1.low > k2.low and k1.high > k2.high: return 'down'
    return 'inclusion'

def kseq_type(k1,k2,k3):
    if k1.low <= k2.low and k1.high<=k2.high and \
       k2.low <= k3.low and k2.high<=k3.high: return 'up'
    elif k1.low >= k2.low and k1.high>=k2.high and \
       k2.low >= k3.low and k2.high>=k3.high: return 'down'
    elif k1.low<k2.low and k1.high<k2.high and \
       k2.low > k3.low and k2.high>k3.high: return 'top'        
    elif k1.low>k2.low and k1.high>k2.high and \
       k2.low < k3.low and k2.high<k3.high: return 'bottom'
    return 'unnormalized'

def kseq_merge(k1,k2,isUp):
    if isUp:
        return K(k2.time,k1.start,max(k1.high,k2.high),k2.end,max(k1.low,k2.low),k1.volume+k2.volume)
    return K(k2.time,k1.start,min(k1.high,k2.high),k2.end,min(k1.low,k2.low),k1.volume+k2.volume)

class KSeq:
    def __init__(self,level,klist):
        self._level = level
##        import pdb;pdb.set_trace()
        if type(klist) is not list: raise TypeError()
        if len(klist)>0 and (type(klist[0]) is not dict) and (type(klist[0]) is not K) and (type(klist[0]) is not tuple):
            raise TypeError()
            
        if len(klist)>0 and type(klist[0]) is dict:
            self._seq = []
            for k in klist:
                self._seq.append(K(k['time'],k['start'],k['high'],k['end'],k['low'],k['volume']))

        if len(klist)>0 and type(klist[0]) is tuple:
            self._seq = []
            for k in klist:
                self._seq.append(K(k[0],k[1],k[2],k[3],k[4],k[5]))
    
        self._low = float('+inf')
        self._high = float('-inf')
        for k in self._seq:
            if k.low < self._low : self._low = k.low
            if k.high > self._high: self._high = k.high
        self._normalize()    

    def addK(self,k):
        self._seq.append(k)
        if k.low < self._low : self._low = k.low
        if k.high > self._high: self._high = k.high
        #adjust last kseq_type
    
    def getDuration(self):
        return {'from':self._seq[0],'to':self._seq[-1]}

    def __getattr__(self,attr):
        if attr=='top': return self._high
        elif attr=='bottom': return self._low

    def _normalize(self):
        self._norm = [self._seq[0]]
        direction = 'up'
        for i in range(1,len(self._seq)):
            ndir = kseq_dir(self._norm[-1],self._seq[i])
            if ndir=='inclusion':
                prev = self._norm[-1]
                nk = kseq_merge(prev,self._seq[i],direction=='up')
                self._seq[i].merged = nk
                if not prev.merged: prev.merged = nk

                nk.merged = True
                if self._norm[-1].ingredient:
                    nk.ingredient = self._norm[-1].ingredient + [i]
                else:
                    nk.ingredient = [i-1,i]

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

                
    
    
      
    

import pandas as pd
import sys




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


##    def __str__(self):
##        return '"time":"'+self.time+'","low":'+str(self.low)+',"high":'+str(self.high)+',"start":'+str(self.start)+',"end":'+str(self.end)+',"volume":'+str(self.volume)

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
                self._seq.append(K(row['date'], row['open'], row['high'], row['close'], row['low'], row['volume']))
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
        if len(self._seq):
            self._normalize()
        self.split2bi()
        self.makeupSegment()
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
    
    def split2bi(self):
        self._bi = []

        if self._norm and len(self._norm) >= 2:
            #looking for first 'up' or down k sequence
            i = 2
            while i < len(self._norm):
                t = kseq_type(self._norm[i-2],self._norm[i-1],self._norm[i])
                if t == 'up': #found up k seq
                    #looking for lowest K backward
                    lowest = (i-2, self._norm[i-2].low)
                    for j in range(i-3, 0, -1):
                        if self._norm[j].low < lowest[1]:
                            lowest = (j, self._norm[j].low)
                    self._bi.append({
                        'from': lowest,
                        'to': (i, self._norm[i].high),
                        'isUp': True,
                        'growing': True
                    })
                    break
                elif t == 'down':
                    #looking for highest K backward
                    highest = (i-2, self._norm[i-2].high)
                    for j in range(i-3, 0, -1):
                        if self._norm[j].high > highest[1]:
                            highest = (j, self._norm[j].high)
                    self._bi.append({
                        'from': highest,
                        'to': (i, self._norm[i].low),
                        'isUp': False,
                        'growing': True
                    })
                    break
                else:
                    i += 1
            #import pdb; pdb.set_trace()
            while i+2 < len(self._norm):                
                t = kseq_type(self._norm[i],self._norm[i+1],self._norm[i+2])
                if self._bi[-1]['isUp']:
                    #import pdb; pdb.set_trace()
                    
                    if t == 'top' and self._norm[i+1].high >= self._bi[-1]['to'][1]:
                        self._bi[-1]['to'] = (i+1,self._norm[i+1].high)
                    elif t == 'bottom' and i+1- self._bi[-1]['to'][0] > 3:
                        self._bi[-1]['growing'] = False
                        self._bi.append({
                            'from': self._bi[-1]['to'],
                            'to': (i+1, self._norm[i+1].low),
                            'isUp': False,
                            'growing': True
                        })
                else:                    
                    #import pdb; pdb.set_trace()
                    if t == 'bottom' and self._norm[i+1].low <= self._bi[-1]['to'][1]:
                        self._bi[-1]['to'] = (i+1,self._norm[i+1].low)
                    elif t == 'top' and i+1- self._bi[-1]['to'][0] > 3:
                        #import pdb; pdb.set_trace()
                        self._bi[-1]['growing'] = False
                        self._bi.append({
                            'from': self._bi[-1]['to'],
                            'to': (i+1, self._norm[i+1].high),
                            'isUp': True,
                            'growing': True
                        })
                i = i + 1

            #map index in _norm into index in _seq
            for i in range(0,len(self._bi)):
                b = self._bi[i]
                if i ==0:
                    if self._norm[b['from'][0]].merged : #
                        if b['isUp']:
                            b['from'] = (self.getRealLowestK(b['from'][0]),b['from'][1])
                        else:
                            b['from'] = (self.getRealHighestK(b['from'][0]),b['from'][1])
                        
                else:
                    b['from'] = self._bi[i-1]['to']
                    
                if self._norm[b['to'][0]].merged:
                    if b['isUp']:
                        b['to'] = (self.getRealHighestK(b['to'][0]),b['to'][1])
                    else:
                        b['to'] = (self.getRealLowestK(b['to'][0]),b['to'][1])
                else:
                    last = self.look4LastMerged(b['to'][0])
                    if last:
                        delta = b['to'][0] - last                        
                        b['to'] = (self._norm[last].ingredient[-1] + delta, b['to'][1])
    def makeupSegment(self):
        self._segment = []
        
        a = self.searchFirstSeg(0)
        if a:
            self._segment.append({
                'from':(self._bi[a['from']]['from'][0],self._bi[a['from']]['from'][1]),
                'to':(self._bi[a['to']]['to'][0],self._bi[a['to']]['to'][1]),
                'isUp': self._bi[a['from']]['isUp'],
                'bi':[k for k in range(a['from'],a['to']+1)],
                'growing':True
                })
            
            i = self._segment[-1]['bi'][-1]
            while i + 3 < len(self._bi):
##                import pdb; pdb.set_trace()
                if self._segment[-1]['isUp']:
                    #looking for top
                    
                    top = self.searchTopSeg(i-1)
                    if top:
                        if top['mode']=='normal':
                            self._segment[-1]['to'] = self._bi[top['biIndex']-1]['to']
                            self._segment[-1]['bi'] += [k for k in range(i+1,top['biIndex'])]
                            self._segment[-1]['growing'] = False
                            #A new segement was born
                            self._segment.append({
                                    'from': self._bi[top['biIndex']]['from'],
                                    'to': self._bi[top['biIndexEnd']]['to'],
                                    'isUp': False,
                                    'bi':[k for k in range(top['biIndex'],top['biIndexEnd']+1)],
                                    'growing':True                            
                                })
                            i = top['biIndexEnd']
                        elif top['mode']=='quekou':
                            #looking for bottom
##                            import pdb; pdb.set_trace()
                            bottom = self.searchBottomSeg(top['biIndex']+1,self._bi[top['biIndex']-2]['from'][1])
                            if bottom and bottom['mode']=='normal':
                                self._segment[-1]['to'] = self._bi[top['biIndex']]['from']
                                self._segment[-1]['bi'] += [k for k in range(i+1,top['biIndex'])]
                                self._segment[-1]['growing'] = False
                                    #A new segement was born
                                self._segment.append({
                                        'from': self._bi[top['biIndex']]['from'],
                                        'to': self._bi[bottom['biIndex']]['from'],
                                        'isUp': False,
                                        'bi':[k for k in range(top['biIndex'],bottom['biIndex'])],
                                        'growing':False                            
                                    })
                                self._segment.append({
                                        'from': self._bi[bottom['biIndex']]['from'],
                                        'to': self._bi[bottom['biIndexEnd']]['to'],
                                        'isUp': True,
                                        'bi':[k for k in range(bottom['biIndex'],bottom['biIndexEnd']+1)],
                                        'growing':True                            
                                    })
                                
                                i = bottom['biIndexEnd']
                            elif bottom and bottom['mode']=='newpeak':
                                self._segment[-1]['to'] = self._bi[bottom['biIndexEnd']]['to']
                                self._segment[-1]['bi'] += [k for k in range(i+1,bottom['biIndexEnd']+1)]
                                i = bottom['biIndexEnd']
                            else:
                                break
                        else:
                            self._segment[-1]['to'] = self._bi[top['biIndexEnd']]['to']
                            self._segment[-1]['bi'] += [k for k in range(i+1,top['biIndexEnd']+1)]
                            i = top['biIndexEnd']
                            break
                    else:
                        break
                else:#down
                    #looking for bottom
##                    import pdb; pdb.set_trace()
                    bottom = self.searchBottomSeg(i-1)
                    if bottom:                        
                        if bottom['mode']=='normal':
                            self._segment[-1]['to'] = self._bi[bottom['biIndex']]['from']
                            self._segment[-1]['bi'] += [k for k in range(i+1,bottom['biIndex'])]
                            self._segment[-1]['growing'] = False
                            #A new segment was born
                            self._segment.append({
                                    'from': self._bi[bottom['biIndex']]['from'],
                                    'to': self._bi[bottom['biIndex']+2]['to'],
                                    'isUp': True,
                                    'bi':[k for k in range(bottom['biIndex'],bottom['biIndex']+3)],
                                    'growing':True                            
                                })
                            i += bottom['biIndex'] + 2
                        elif bottom['mode'] == 'quekou':
##                            import pdb; pdb.set_trace()
                            top = self.searchTopSeg(bottom['biIndex']+1)
                            if top: #the segment is dead
                                self._segment[-1]['to'] = self._bi[bottom['biIndex']]['from']
                                self._segment[-1]['bi'] += [k for k in range(i+1,bottom['biIndex'])]
                                
                                self._segment[-1]['growing'] = False
                                #A new segment was born
                                self._segment.append({
                                        'from': self._bi[bottom['biIndex']]['from'],
                                        'to': self._bi[top['biIndexEnd']]['to'],
                                        'isUp': True,
                                        'bi':[k for k in range(bottom['biIndex'],top['biIndexEnd']+1)],
                                        'growing':True                            
                                    })
                                i = top['biIndexEnd']
                            else:
                                break
                        else:
                            self._segment[-1]['to'] = self._bi[bottom['biIndexEnd']]['to']
                            self._segment[-1]['bi'] += [k for k in range(i+1,bottom['biIndexEnd']+1)]
                            break                        
                    else:
                        # new peak
##                        import pdb; pdb.set_trace()
                        if top['biIndexEnd'] + 1 < len(self._bi) \
                            and self._bi[top['biIndexEnd']+1]['from'][1] > self._bi[top['biIndex']]['from'][1]:
                            self._segment[-1]['to'] = self._bi[bottom['biIndex']]['from']
                            self._segment[-1]['bi'] += [k for k in range(i+1,bottom['biIndex'])]

                        break
                    
    def searchBottomSeg(self,start,quekou=None):
        assert(start<len(self._bi) and self._bi[start]['isUp'])
        prev = {'biIndex':start,'to':self._bi[start]['to'][1],'from':self._bi[start]['from'][1]}
        current = None
        i = start + 2;
        while i < len(self._bi):
            val = current
            if not val: val = prev
            
##            if i+2 == len(self._bi) and self._bi[i+1]['to'][1] < prev['from']:
##                return {'biIndex':prev['biIndex'], 'biIndexEnd':i+1,'mode':"newpeak"}

            t = biseq_dir(val['from'],val['to'],self._bi[i]['from'][1],self._bi[i]['to'][1])
            if t == 'inclusion':
                if self._bi[i]['from'][1] > self._bi[i-2]['from'][1]:#included by left
                    val['from'] = min(val['from'],self._bi[i]['from'][1])
                    val['to'] = min(val['to'],self._bi[i]['to'][1])
                    i += 2
                    continue
                else: #included by right
##                    #check if previous segment is broken by next bi
##                    if self._bi[i]['to'][1] > self._segment[-1]['from']:
##                        to = self.checkFirstSeg(i)                    
##                        if to:
##                            return {'biIndex':i, 'biIndexEnd':i,'mode':"newpeak"}
                    to = self.checkFirstSeg(i)                    
                    if to:
                        if not quekou:
                            return {'biIndex':i, 'biIndexEnd':to,'mode':"normal"}
                        else:
                            if self._bi[to]['to'] > self._segment[-1]['to'] and self._bi[i-1]['to'][1] > quekou :#previous segment continue
                                return {'biIndex':i, 'biIndexEnd':to,'mode':"newpeak"}
                    else: # new high
                            prev = {'biIndex':i,'to':self._bi[i]['to'][1],'from':self._bi[i]['from'][1]}
                            current = None
                            if i+2 == len(self._bi) and self._bi[i+1]['to'][1] < prev['from']:
                                return {'biIndex':i, 'biIndexEnd':i,'mode':"newpeak"}
                            i += 2
            else:
                if not current:
                    current = {'biIndex':i,'to':self._bi[i]['to'][1],'from':self._bi[i]['from'][1]}
                    i += 2
                    continue
                #evaluate type
                if current['from'] < prev['from'] and current['from'] < self._bi[i]['from'][1] \
                    and current['to'] < prev['to'] and current['to'] < self._bi[i]['to'][1]:#bottom
                    return {'biIndex':current['biIndex'],'biIndexEnd':i, 'mode': 'quekou'if current['to'] < prev['from'] else 'normal'}
                prev = current
                current = {'biIndex':i,'from':self._bi[i]['from'][1],'to':self._bi[i]['to'][1]}
                i += 2

        #
                
    def searchTopSeg(self,start):
        
        assert(start<len(self._bi) and self._bi[start]['isUp']==False)
        prev = {'biIndex':start,'to':self._bi[start]['to'][1],'from':self._bi[start]['from'][1]}
        current = None
        i = start + 2;
        while i < len(self._bi):
            val = current
            if not val: val = prev

            if i+2 == len(self._bi) and self._bi[i+1]['to'][1] > prev['from']:
                return {'biIndex':prev['biIndex'], 'biIndexEnd':i+1,'mode':"newpeak"}
            
            t = biseq_dir(val['from'],val['to'],self._bi[i]['from'][1],self._bi[i]['to'][1])
            if t == 'inclusion':
                if self._bi[i]['to'][1] > self._bi[i-2]['to'][1]:
                    val['from'] = max(val['from'],self._bi[i]['from'][1])
                    val['to'] = max(val['to'],self._bi[i]['to'][1])
                    i += 2
                    continue
                else:
                    to = self.checkFirstSeg(i)
                    
                    if to:
                        return {'biIndex':i, 'biIndexEnd':to,'mode':"normal"}
                    else: # new high
                        prev = {'biIndex':i,'to':self._bi[i]['to'][1],'from':self._bi[i]['from'][1]}
                        current = None
                        if i+2 == len(self._bi) and self._bi[i+1]['to'][1] > prev['from']:
                            return {'biIndex':i, 'biIndexEnd':i,'mode':"newpeak"}
                        i += 2
            else:
##                import pdb; pdb.set_trace()
                if not current:
                    current = {'biIndex':i,'to':self._bi[i]['to'][1],'from':self._bi[i]['from'][1]}
                    i += 2
                    continue

                #evaluate type
                if current['to'] > prev['to'] and current['to'] > self._bi[i]['to'][1] \
                      and current['from'] > prev['from'] and current['from'] > self._bi[i]['from'][1]:#top
                    return {'biIndex':current['biIndex'],'biIndexEnd':i, 'mode': 'quekou' if current['to'] > prev['from'] else 'normal'}
                prev = current
                current = {'biIndex':i,'from':self._bi[i]['from'][1],'to':self._bi[i]['to'][1]}
                i += 2

    def searchFirstSeg(self,start):
        i = start
        while i+2 < len(self._bi):
            seg = self.checkFirstSeg(i)
            if seg:
                return {'from':i,'to':seg}
            i += 1
            
    def checkFirstSeg(self,start):
        isUp = self._bi[start]['isUp']
        first = {'biIndex':start,'to':self._bi[start]['to'][1],'from':self._bi[start]['from'][1]}

        i = start + 2;
        if isUp:
            while i < len(self._bi):
                second = {'biIndex':i,'to':self._bi[i]['to'][1],'from':self._bi[i]['from'][1]}
                
                t = biseq_dir(first['from'],first['to'],second['from'],second['to'])
                if t == 'up':
                    return i
                elif t == 'down':
                    return None
                elif t == 'inclusion' and second['from'] > first['from']: #forward inclusion
                        i += 2
                        continue #ignore the second
                else: #backward inclusion
                    return None
        else:
            while i < len(self._bi):
                second = {'biIndex':i,'to':self._bi[i]['to'][1],'from':self._bi[i]['from'][1]}
                
                t = biseq_dir(first['from'],first['to'],second['from'],second['to'])
                if t == 'down':
                    return i
                elif t == 'up':
                    return None
                elif t == 'inclusion':
                    if second['from'] < first['from']: #forward inclusion
                        i += 2
                        continue #ignore the second
                    else: #backward inclusion
                        return None
                
def biseq_dir(n1,n2,n3,n4):
    if n1 > n3 and n2 > n4:
        return 'down'
    elif n1 < n3 and n2 < n4:
        return 'up'
    return 'inclusion'

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



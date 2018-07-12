class Segment:
    def __init__(self,strokes,begin,end,lastTrait=None):
        self._strokes = strokes
        self._begin = begin
        self._end = end
        self.direction = 'unknown'
        self.status = 'conception' 
        if 2 < len(strokes)-begin:
            self.direction = 'up' if strokes[begin]['isUp'] else 'down'
            self.status = 'growing'
            if lastTrait:
                self._lastTrait = lastTrait
            else:
                self._lastTrait = strokes[self._end-2]
        self.brokenBy = None
##        assert(self.isValid())
        if not self.isValid():
            import pdb;pdb.set_trace()
    def __str__(self):
        return '{' + \
               '"from":'+str(self._strokes[self._begin]['from']) + ','+\
               '"to":'+str(self._strokes[self._end-1]['to']) + ','+\
               '"isUp":'+str(self.direction=='up')+','+\
               '"bi":'+str([k for k in range(self._begin,self._end)])+','+\
               '"growing":'+str(self.status=='growing')+\
               '}'

    def __repr__(self):
        return str(self)
    
    def isValid(self):
        #1 clear direction
        if self.direction != 'up' and self.direction != 'down':
            return False
        
        #2 having odd of strokes more than 3
        num = self._end-self._begin
        if  num < 3 or num %2 == 0:
            return False
        for i in range(self._begin+2,self._end):
            g1 = max(self._strokes[i-2]['from'][1],self._strokes[i-2]['to'][1])
            g2 = max(self._strokes[i]['from'][1],self._strokes[i]['to'][1])
            d1 = min(self._strokes[i-2]['from'][1],self._strokes[i-2]['to'][1])
            d2 = min(self._strokes[i]['from'][1],self._strokes[i]['to'][1])
            if min(g1,g2) < max(d1,d2):  return False

        #3 dirction
        if self._strokes[self._begin]['isUp'] and self.direction != 'up':
            return False
        if not self._strokes[self._begin]['isUp'] and self.direction != 'down':
            return False

        #4 status
        if self.status == 'mature' and \
           (not self.brokenBy or not self.brokenBy.isValid()):
            return False
        return True



    def __getattr__(self, attr):
        if attr == 'lastTrait':
            return self._lastTrait
        elif attr == 'numOfStrokes':
            return self._end - self._begin
        elif attr == 'firstStroke':
            return self._strokes[self._begin]
        elif attr == 'lastStroke':
            return self._strokes[self._end-1]
        elif attr == 'lastPeak':
            return self._lastTrait['from'][1]
        elif attr == 'from':
            return self._strokes[self._begin]['from']
        elif attr == 'to':
            return self._strokes[self._end-1]['to']
        elif attr == 'growing':
            return self.status == 'growing'

    def __getitem__(cls, x):
            return getattr(cls, x)

    def grows(self,lastTrait,step=None):
        assert(self.status == 'growing')
        if not step:
            step = lastTrait['hops']+1 if 'hops' in lastTrait.keys() else 2

        if self._end + step > len(self._strokes):
            import pdb;pdb.set_trace()
        self._end += step
        self._lastTrait = lastTrait
        
    def mature(self, brokenBy):
        self.status = 'mature'
        self.brokenBy = brokenBy


def strokes_dir(n1,n2,n3,n4):
    if n1 > n3 and n2 > n4:
        return 'down'
    elif n1 < n3 and n2 < n4:
        return 'up'
    return 'inclusion'

def resolveSeg(strokes,begin,end, segs ,currentSeg = None, prevSeg = None):
    if end-begin < 2:
        return
    assert(len(strokes)>begin)
    assert(len(strokes)<=end)
    
##    import pdb;pdb.set_trace()

    if not prevSeg:
        if not currentSeg:
            #first segment
            i = 0
            while i < (end-begin):
                nextSeg = locateSimpleSeg(strokes,begin+i)
                if not nextSeg:
                    i += 1
                else:
                    break
            if not nextSeg:
                return 
            segs.append(nextSeg)
            return resolveSeg(strokes,begin+i+nextSeg.numOfStrokes,end,segs,nextSeg)
        else:
            prevTrait = currentSeg.lastTrait
            if currentSeg: isUp = currentSeg.direction == 'up'
            else: isUp = strokes[begin]['isUp']
            
            if isUp:
            # up case                
                currentTrait = strokes[begin]
                t = strokes_dir(prevTrait['from'][1],prevTrait['to'][1],currentTrait['from'][1],currentTrait['to'][1])
##                assert('up'== t or (t == 'inclusion' and  currentTrait['from'][1] >prevTrait['from'][1] ))
                iPeak = 0
                i = 2
                while True:
                    if i > (end-begin): break
                    if i==(end-begin):
                        currentSeg.grows(currentTrait,i)
                        break
                    
                    nextTrait = strokes[begin+i]
                    t = strokes_dir(currentTrait['from'][1],currentTrait['to'][1],nextTrait['from'][1],nextTrait['to'][1])
                    if t == 'up': #case 1: new peak
                        prevTrait = currentTrait
                        currentTrait = nextTrait
                        currentSeg.grows(prevTrait)
                        i += 2
                        iPeak += (2 if (not 'hops' in prevTrait.keys()) else prevTrait['hops']+1)
                    elif t == 'inclusion' and strokes[begin+i]['to'][1] >= currentTrait['to'][1]:#included in left
                        if currentTrait['to'][1] < currentSeg.firstStroke['from'][1] and \
                           strokes[begin+i]['to'][1] < currentSeg.firstStroke['from'][1]:
                            #breaks previous segment start by first stroke => treat as
                            nextSeg = Segment(strokes,begin,begin+i+1,{'from':(currentTrait['from'][0],nextTrait['from'][1]+0.01), 'to':nextTrait['from']})
                            currentSeg.mature(nextSeg)
                            segs.append(nextSeg)
                            return resolveSeg(strokes,begin+nextSeg.numOfStrokes,end,segs,nextSeg)
                        else:
                            hops = currentTrait['hops']+2 if 'hops' in currentTrait.keys() else 3
                            currentTrait = { 'from':currentTrait['from'],
                                             'to':(nextTrait['to'][0],currentTrait['to'][1]),
                                             'hops':hops}
                            i += 2
                    elif t == 'inclusion' and strokes[i]['to'][1] < currentTrait['to'][1]:#case 3：included in right
                        #same as 'up'
                        prevTrait = currentTrait
                        currentTrait = nextTrait
                        currentSeg.grows(prevTrait)
                        i += 2
                        iPeak += (2 if (not 'hops' in prevTrait.keys()) else prevTrait['hops']+1)
                    elif t == 'down':#case 2
##                        hops = prevTrait['hops']+1 if 'hops' in prevTrait.keys() else 2
                        hops = prevTrait['hops']+1 if 'hops' in prevTrait.keys() else 2
                        
                        nextSeg = Segment(strokes,begin+iPeak,begin+i+1)
                        if currentTrait['to'][1] <= currentSeg.lastPeak:
                            #first stroke breaks previous segment       
                            currentSeg.mature(nextSeg)
                            segs.append(nextSeg)
                            return resolveSeg(strokes,begin+i+1,end,segs,nextSeg)
                        else:
                            return resolveSeg(strokes,begin+i+1,end,segs,nextSeg,currentSeg)
                        
            else: #down case
                currentTrait = strokes[begin]
                
                t = strokes_dir(prevTrait['from'][1],prevTrait['to'][1],currentTrait['from'][1],currentTrait['to'][1])
##                assert('down'==t or ( t == 'inclusion' and currentTrait['from'][1] < prevTrait['from'][1]))
                iPeak = 0
                i = 2
                while True:
                    if i > (end-begin): break
                    if i==(end-begin):
                        currentSeg.grows(currentTrait,i)
                        return

                    nextTrait = strokes[begin+i]
                    t = strokes_dir(currentTrait['from'][1],currentTrait['to'][1],nextTrait['from'][1],nextTrait['to'][1])
                    if t == 'down': #case 1: new peak
                        prevTrait = currentTrait
                        currentTrait = nextTrait
                        currentSeg.grows(prevTrait)
                        i += 2
                        iPeak += (2 if (not 'hops' in prevTrait.keys()) else prevTrait['hops']+1)
                    elif t == 'inclusion' and nextTrait['to'][1] <= currentTrait['to'][1]:#included in left
                        if currentTrait['to'][1] > currentSeg.firstStroke['from'][1] and \
                           strokes[begin+i]['to'][1] > currentSeg.firstStroke['from'][1]:
                            #breaks previous segment start by first stroke => treat as
                            nextSeg = Segment(strokes,begin,begin+i+1,{'from':(currentTrait['to'][0],nextTrait['to'][1]-0.01), 'to':nextTrait['from']})
                            currentSeg.mature(nextSeg)
                            segs.append(nextSeg)
                            return resolveSeg(strokes,begin+nextSeg.numOfStrokes,end,segs,nextSeg)
                        else:
                            hops = currentTrait['hops']+2 if 'hops' in currentTrait.keys() else 3
                            currentTrait = { 'from':currentTrait['from'],
                                             'to':(nextTrait['to'][0],currentTrait['to'][1]),
                                             'hops':hops}
                            i += 2
                    elif t == 'inclusion' and nextTrait['to'][1] > currentTrait['to'][1]:#case 3：included in right
                        #same as 'up'
                        prevTrait = currentTrait
                        currentTrait = nextTrait
                        currentSeg.grows(prevTrait)
                        i += 2
                        iPeak += (2 if (not 'hops' in prevTrait.keys()) else prevTrait['hops']+1)
                    elif t == 'up':#case 2
##                        hops = prevTrait['hops']+1 if 'hops' in prevTrait.keys() else 2
                        hops = prevTrait['hops']+1 if 'hops' in prevTrait.keys() else 2
                        
                        nextSeg = Segment(strokes,begin+iPeak,begin+i+1)
                        if currentTrait['to'][1] >= currentSeg.lastPeak:
                            #first stroke breaks previous segment       
                            currentSeg.mature(nextSeg)
                            segs.append(nextSeg)
                            return resolveSeg(strokes,begin+i+1,end,segs,nextSeg)
                        else:
                            return resolveSeg(strokes,begin+i+1,end,segs,nextSeg,currentSeg)                     
    else:#
        assert(prevSeg.status == 'growing')
        assert(currentSeg.status == 'growing')
        if currentSeg.direction == 'down':
            assert(prevSeg.direction == 'up')
            assert(currentSeg.firstStroke['to'][1] > prevSeg.lastPeak)
            prevTrait = currentSeg.lastTrait
            currentTrait = strokes[begin]
            i = 2
            iPeak = 0
            while True:
                if i > (end-begin): break
                if i==(end-begin):
                    currentSeg.grows(currentTrait,i-iPeak)
                    break
                
                nextTrait = strokes[begin+i]
                t = strokes_dir(currentTrait['from'][1],currentTrait['to'][1],nextTrait['from'][1],nextTrait['to'][1])
                if t == 'down': #case 1: new peak for currentSeg
                    if nextTrait['from'][1] < prevSeg['from'][1]:#breaks start, prevSeg was broken
                        currentSeg.grows(currentTrait)
                        prevSeg.mature(currentSeg)
                        segs.append(currentSeg)
                        return resolveSeg(strokes,begin+i,end,segs,currentSeg)
                    else:
                        prevTrait = currentTrait
                        currentTrait = nextTrait
                        currentSeg.grows(prevTrait)
                        i += 2
                        iPeak += (2 if (not 'hops' in prevTrait.keys()) else prevTrait['hops']+1)
                elif t == 'inclusion' and strokes[begin+i]['to'][1] <= currentTrait['to'][1]:#included in left
                    hops = currentTrait['hops']+2 if 'hops' in currentTrait.keys() else 3
                    currentTrait = { 'from':currentTrait['from'], 'to':strokes[begin+i]['to'],'hops':hops}
                    i += 2
                elif t == 'inclusion' and strokes[begin+i]['to'][1] < currentTrait['to'][1]:#case 3：included in right
                    #same as 'down'
                    prevTrait = currentTrait
                    currentTrait = nextTrait
                    currentSeg.grows(currentTrait)
                    i += 2
                    iPeak += (2 if (not 'hops' in prevTrait.keys()) else prevTrait['hops']+1)
                elif t == 'up':#bottom
                    if nextTrait['to'][1] <= currentSeg.firstStroke['from'][1]:
                        nextSeg = Segment(strokes,begin+iPeak,begin+i+1)                      
                        prevSeg.mature(currentSeg)
                        currentSeg.mature(nextSeg)
                        segs.append(currentSeg)
                        segs.append(nextSeg)
                        return resolveSeg(strokes,begin+i+1,end,segs,nextSeg)
                    else:#new peak for prevSeg
                        prevSeg.grows(strokes[begin+i-1],currentSeg.numOfStrokes+i+1)
                        return resolveSeg(strokes,begin+i+1,end,segs,prevSeg)
                        
        else:#up
            assert(prevSeg.direction == 'down')
            assert(currentSeg.firstStroke['to'][1] < prevSeg.lastPeak)
            prevTrait = currentSeg.lastTrait
            currentTrait = strokes[begin]
            i = 2
            iPeak = 0
            while True:
                if i > (end-begin): break
                if i==(end-begin):
                    currentSeg.grows(currentTrait,i-iPeak)
                    return
                nextTrait = strokes[begin+i]
                t = strokes_dir(currentTrait['from'][1],currentTrait['to'][1],nextTrait['from'][1],nextTrait['to'][1])
                if t == 'up': #case 1: new peak
                    if nextTrait['from'][1] > prevSeg['from'][1]:#breaks start, prevSeg was broken
                        currentSeg.grows(currentTrait)
                        prevSeg.mature(currentSeg)
                        segs.append(currentSeg)
                        return resolveSeg(strokes,begin+i,end,segs,currentSeg)
                    else:
                        prevTrait = currentTrait
                        currentTrait = nextTrait
                        currentSeg.grows(prevTrait)
                        i += 2
                        iPeak += (2 if (not 'hops' in prevTrait.keys()) else prevTrait['hops']+1)
                elif t == 'inclusion' and strokes[begin+i]['to'][1] >= currentTrait['to'][1]:#included in left
                    hops = currentTrait['hops']+2 if 'hops' in currentTrait.keys() else 3
                    currentTrait = { 'from':currentTrait['from'], 'to':strokes[begin+i]['to']}
                    i += 2
                elif t == 'inclusion' and strokes[begin+i]['to'][1] < currentTrait['to'][1]:#case 3：included in right
                    #same as 'up'
                    prevTrait = currentTrait
                    currentTrait = nextTrait
                    currentSeg.grows(currentTrait)
                    i += 2
                    iPeak += (2 if (not 'hops' in prevTrait.keys()) else prevTrait['hops']+1)
                elif t == 'down':#top
                    if nextTrait['to'][1] >= currentSeg.firstStroke['from'][1]:
                        nextSeg = Segment(strokes,begin+iPeak,begin+i+1)
                        prevSeg.mature(currentSeg)
                        currentSeg.mature(nextSeg)
                        segs.append(currentSeg)
                        segs.append(nextSeg)
                        return resolveSeg(strokes,begin+i+1,end,segs,nextSeg)
                    else:
                        prevSeg.grows(strokes[begin+i-1],currentSeg.numOfStrokes+i+1)
                        return resolveSeg(strokes,begin+i+1,end,segs,prevSeg)
    
def locateSimpleSeg(strokes,begin):
    if len(strokes)-begin < 3: return
    return locateSimpleUp(strokes,begin) if strokes[begin]['isUp'] else locateSimpleDown(strokes,begin)

def locateSimpleUp(strokes,begin):
    g = strokes[begin]['to'][1]
    d = strokes[begin]['from'][1]
    prev = (strokes[begin]['from'][1],strokes[begin]['to'][1])
    for i in range(2,len(strokes)-begin,2):
        if strokes[begin+i]['from'][1] < prev[0]: #break wrong end
            return None
        if strokes[begin+i]['to'][1] > prev[1]:            
            return Segment(strokes,begin,begin+i+1)

    return None

def locateSimpleDown(strokes,begin):
    g = strokes[begin]['from'][1]
    d = strokes[begin]['to'][1]
    prev = (g,d)
    for i in range(2,len(strokes)-begin,2):
        if strokes[begin+i]['from'][1] > prev[0]: #break wrong end
            return None
        if strokes[begin+i]['to'][1] < prev[1]:            
            return Segment(strokes,begin,begin+i+1)

    return None

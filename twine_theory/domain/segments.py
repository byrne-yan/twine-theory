class Segment:
    def __init__(self,strokes):
        self._strokes = strokes
        self._direction = 'unknown'
        self.status = 'conception' # born, mature
        self.brokenBy = None
        
        
    def isValid(self):
        #1 clear direction
        if self.direction != 'up' and self.direction != 'down':
            return False
        
        #2 having odd of strokes more than 3
        num = len(self._strokes)
        if  num < 3 or num %2 == 0:
            return False
        for i in range(1,len(self._strokes)):
            g1 = max(self._strokes[i-1]['from'][1],self._strokes[i-1]['to'][1])
            g2 = max(self._strokes[i]['from'][1],self._strokes[i]['to'][1])
            d1 = min(self._strokes[i-1]['from'][1],self._strokes[i-1]['to'][1])
            d2 = min(self._strokes[i]['from'][1],self._strokes[i]['to'][1])
            if min(g1,g2) < min(g1,g2):  return False

        #3 dirction
        if self._strokes[0]['isUp'] and self.status != 'up':
            return False
        if not self._strokes[0]['isUp'] and self.status != 'down':
            return False

        #4 status
        if self.status == 'mature' and \
           (not self.brokenBy or not self.brokenBy.isValid()):
            return False
        return True



    def __getattr__(self, attr):
        if attr == 'direction':
            return self._diection
        elif attr == 'lastTrait':
            return self._lastTrait
        elif attr == 'numOfStrokes':
            return len(self._strokes)

    def grows(self,strokes,lastTrait):
        assert(self.status == 'growing')
        assert(2 == len(strokes))
        self._strokes += strokes
        self._lastTrait = lastTrait
        
    def mature(self, brokenBy):
        self.status = 'mature'
        self.brokenBy = brokenBy
        self.

def strokes_dir(n1,n2,n3,n4):
    if n1 > n3 and n2 > n4:
        return 'down'
    elif n1 < n3 and n2 < n4:
        return 'up'
    return 'inclusion'

def resolveSeg(strokes, currentSeg = None, prevSeg = None):
    mySegs = []

    if not prevSeg:
        if not currentSeg: #first segment
            seg = locateSimpleSeg(strokes)
            mySeg += seg
            mySeg += resolveSeg(strokes[seg.numOfStrokes:],seg)
        else:
            prevTrait = currentSeg.lastTrait
            currentTrait = strokes[0]
            assert('up'==strokes_dir(prevTrait['from'],prevTrait['to'],currentTrait['from'],currentTrait['to']))
            i = 2
            while i < len(strokes):
                nextTrait = strokes[i]
                t = strokes_dir(currentTrait['from'],currentTrait['to'],nextTrait['from'],nextTrait['to'])
                if t == 'up': #new peak
                    prevTrait = currentTrait
                    currentTrait = nextTrait
                    currentSeg.grows(strokes[i-2:i],currentTrait)
                    i += 2
                elif t == 'inclusion' and strokes[i]['to'] >= currentTrait['to']:#included in left
                    currentTrait = { 'from':currentTrait['from'], 'to':strokes[i]['to']}
                    i += 2
                
                elif t == 'inclusion' and strokes[i]['to'] < currentTrait['to']:#included in right
                elif t == 'down':#top
                    seg = Segment(strokes[0:i])
                    if currentTrait['to'] <= currentSeg.lastPeak: #case 1                        
                        currentSeg.setBrokenBy(seg)
                        mySegs += [seg]
                        j = i
                        while j<len(strokes):
                            nextSeg = resolveSeg(strokes[j:],seg)
                            if len(nextSeg) == 0:
                                return mySegs
                            mySegs += nextSeg
                            for s in nextSeg:                                
                                j += len(s.numOfStrokes)                                                         
                    else                        
                        if currentSeg.brokenBy == nextSeg
                
    if not currentSeg:
        currentSeg = locateSimpleSeg(strokes)
        myStrokes = strokes[currentSeg.numOfStrokes:]

    nextSeg = locateSimpleSeg(myStrokes)
    if currentSeg.checkBrokenBy(nextSeg):#case 1
        currentSeg.mature(nextSeg)
        mySegs += [currentSeg,nextSeg]
    else:
        if not prevSeg:
            segs = resolveSeg(myStrokes[],nextSeg,currentSeg)
            if segs: mySegs += segs
        else:
        assert(prevSeg.isValid())
        #check if currentSeg breaks the prevSeg
        if prevSeg.diection == 'up':
            if currentSeg.firstStroke <= preseg.lastPeak and currentSeg.secondStroke <= preseg.lastPeak:
                prevSeg.mature(currentSeg)
                mySegs += [prevSeg,currentSeg]
                prevSeg = currentSeg
                
    return mySegs
    
def locateSimpleSeg(strokes):
    assert(len(strokes) > 2)
    return locateSimpleUp(strokes) if strokes[0]['isUp'] else locateSimpleDown(strokes)

def locateSimpleUp(strokes):
    g = strokes[0]['to'][1]
    d = strokes[0]['from'][1]
    prev = (strokes[0]['from'][1],strokes[0]['to'][1])
    for i in range(2,len(strokes),2):
        if strokes[i]['from'][1] < prev[0]: #break wrong end
            return None
        if strokes[i]['to'][1] > prev[1]:            
            return Segment(strokes[:i])

    return None

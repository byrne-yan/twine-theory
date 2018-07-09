class Segment:
    def __init__(self,strokes,lastTrait=None):
        self._strokes = strokes
        self.direction = 'unknown'
        self.status = 'conception' 
        if 2 < len(strokes):
            self.direction = 'up' if strokes[0]['isUp'] else 'down'
            self.status = 'growing'
            if lastTrait:
                self._lastTrait = lastTrait
            else:
                self._lastTrait = strokes[-2]
        self.brokenBy = None
        assert(self.isValid())
        
    def isValid(self):
        #1 clear direction
        if self.direction != 'up' and self.direction != 'down':
            return False
        
        #2 having odd of strokes more than 3
        num = len(self._strokes)
        if  num < 3 or num %2 == 0:
            return False
        for i in range(2,len(self._strokes)):
            g1 = max(self._strokes[i-2]['from'][1],self._strokes[i-2]['to'][1])
            g2 = max(self._strokes[i]['from'][1],self._strokes[i]['to'][1])
            d1 = min(self._strokes[i-2]['from'][1],self._strokes[i-2]['to'][1])
            d2 = min(self._strokes[i]['from'][1],self._strokes[i]['to'][1])
            if min(g1,g2) < min(g1,g2):  return False

        #3 dirction
        if self._strokes[0]['isUp'] and self.direction != 'up':
            return False
        if not self._strokes[0]['isUp'] and self.direction != 'down':
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
            return len(self._strokes)
        elif attr == 'firstStroke':
            return self._strokes[0]
        elif attr == 'lastPeak':
            return self._lastTrait['from'][1]


    def grows(self,strokes,lastTrait):
        assert(self.status == 'growing')
        assert(2 == len(strokes))
        self._strokes += strokes
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

def resolveSeg(strokes, segs = [],currentSeg = None, prevSeg = None):
    if len(strokes) < 2:
        return
    
    if not prevSeg:
        if not currentSeg:
            #first segment
            nextSeg = locateSimpleSeg(strokes)
            segs += [nextSeg]
            resolveSeg(strokes[nextSeg.numOfStrokes:],segs,nextSeg)
        else:
            prevTrait = currentSeg.lastTrait
            if (currentSeg and currentSeg.direction == 'up' ) or \
               (not currentSeg and strokes[0]['isUp']):
            # up case
                
                currentTrait = strokes[0]
                assert('up'==strokes_dir(prevTrait['from'][1],prevTrait['to'][1],currentTrait['from'][1],currentTrait['to'][1]))
                i = 2
                while i < len(strokes):
                    nextTrait = strokes[i]
                    t = strokes_dir(currentTrait['from'][1],currentTrait['to'][1],nextTrait['from'][1],nextTrait['to'][1])
                    if t == 'up': #case 1: new peak
                        prevTrait = currentTrait
                        currentTrait = nextTrait
                        currentTrait['endIndex'] = i
                        currentSeg.grows(strokes[i-2:i],currentTrait)
                        i += 2
                    elif t == 'inclusion' and strokes[i]['to'] >= currentTrait['to']:#included in left
                        currentTrait = { 'from':currentTrait['from'], 'to':strokes[i]['to'],'endIndex':i}
                        i += 2                    
                    elif t == 'inclusion' and strokes[i]['to'] < currentTrait['to']:#case 3：included in right
                        #same as 'up'
                        prevTrait = currentTrait
                        currentTrait = nextTrait
                        currentTrait['endIndex'] = i
                        currentSeg.grows(strokes[i-2:i+1],currentTrait)
                        i += 2                        
                    elif t == 'down':#case 2
                        nextSeg = Segment(strokes[0:i+1])
                        if currentTrait['to'][1] <= currentSeg.lastPeak:
                            #first stroke breaks previous segment       
                            currentSeg.mature(nextSeg)
                            segs += [nextSeg]
                            resolveSeg(strokes[i+nextSeg.numOfStrokes:],segs,nextSeg)
                        else:
                            resolveSeg(strokes[i+seg.numOfStrokes:],segs,nextSeg,currentSeg)
                        break
            elif (currentSeg and currentSeg.direction == 'down' ) or \
               (not currentSeg and strokes[0]['isUp'] == False):
            #down case
                currentTrait = strokes[0]
                currentTrait['endIndex'] = 0
                assert('down'==strokes_dir(prevTrait['from'],prevTrait['to'],currentTrait['from'],currentTrait['to']))
                i = 2
                while i < len(strokes):
                    nextTrait = strokes[i]
                    t = strokes_dir(currentTrait['from'],currentTrait['to'],nextTrait['from'],nextTrait['to'])
                    if t == 'down': #case 1: new peak
                        prevTrait = currentTrait
                        currentTrait = nextTrait
                        currentTrait['endIndex'] = i
                        currentSeg.grows(strokes[i-2:i],currentTrait)
                        i += 2
                    elif t == 'inclusion' and strokes[i]['to'] >= currentTrait['to']:#included in left
                        currentTrait = { 'from':currentTrait['from'], 'to':strokes[i]['to'],'endIndex':i}
                        i += 2                    
                    elif t == 'inclusion' and strokes[i]['to'] < currentTrait['to']:#case 3：included in right
                        #same as 'up'
                        prevTrait = currentTrait
                        currentTrait = nextTrait
                        currentTrait['endIndex'] = i
                        currentSeg.grows(strokes[i-2:i],currentTrait)
                        i += 2                        
                    elif t == 'up':#case 2
                        nextSeg = Segment(strokes[i:i+2],currentTrait['endIndex'])
                        if currentTrait['to'] >= currentSeg.lastPeak:
                            #first stroke breaks previous segment       
                            currentSeg.mature(nextSeg)
                            segs += [nextSeg]
                            resolveSeg(strokes[i+nextSeg.numOfStrokes:],segs,nextSeg)
                        else:
                            resolveSeg(strokes[i+seg.numOfStrokes:],segs,nextSeg,currentSeg)
                        break
                
    else:#
        assert(prevSeg.status == 'growing')
        assert(currentSeg.status == 'growing')
        if currentSeg.direction == 'down':
            assert(prevSeg.direction == 'up')
            assert(currentSeg.firstStroke['to'] > prevSeg.lastPeak)
            currentTrait = strokes[0]
            currentTrait['endIndex'] = 0
            i = 2
            while i < len(strokes):
                nextTrait = strokes[i]
                t = strokes_dir(currentTrait['from'],currentTrait['to'],nextTrait['from'],nextTrait['to'])
                if t == 'down': #case 1: new peak
                    prevTrait = currentTrait
                    currentTrait = nextTrait
                    currentTrait['endIndex'] = i
                    currentSeg.grows(strokes[i-2:i],currentTrait)
                    i += 2
                elif t == 'inclusion' and strokes[i]['to'] >= currentTrait['to']:#included in left
                    currentTrait = { 'from':currentTrait['from'], 'to':strokes[i]['to'],'endIndex':i}
                    i += 2                    
                elif t == 'inclusion' and strokes[i]['to'] < currentTrait['to']:#case 3：included in right
                    #same as 'up'
                    prevTrait = currentTrait
                    currentTrait = nextTrait
                    currentTrait['endIndex'] = i
                    currentSeg.grows(strokes[i-2:i],currentTrait)
                    i += 2                        
                elif t == 'up':#case 2
                    nextSeg = Segment(strokes[i:i+2],currentSegment['endIndex'])
                    preSeg.mature(currentSeg)
                    currentSeg.mature(nextSeg)
                    segs += [currentSeg,nextSeg]
                    resolveSeg(strokes[i+nextSeg.numOfStrokes:],segs,nextSeg)
                    break
        else:#up
            assert(prevSeg.direction == 'down')
            assert(currentSeg.firstStroke['to'] < prevSeg.lastPeak)
            currentTrait = strokes[0]
            currentTrait['endIndex'] = 0
            i = 2
            while i < len(strokes):
                nextTrait = strokes[i]
                t = strokes_dir(currentTrait['from'],currentTrait['to'],nextTrait['from'],nextTrait['to'])
                if t == 'up': #case 1: new peak
                    prevTrait = currentTrait
                    currentTrait = nextTrait
                    currentTrait['endIndex'] = i
                    currentSeg.grows(strokes[i-2:i],currentTrait)
                    i += 2
                elif t == 'inclusion' and strokes[i]['to'] >= currentTrait['to']:#included in left
                    currentTrait = { 'from':currentTrait['from'], 'to':strokes[i]['to'],'endIndex':i}
                    i += 2                    
                elif t == 'inclusion' and strokes[i]['to'] < currentTrait['to']:#case 3：included in right
                    #same as 'up'
                    prevTrait = currentTrait
                    currentTrait = nextTrait
                    currentTrait['endIndex'] = i
                    currentSeg.grows(strokes[i-2:i],currentTrait)
                    i += 2                        
                elif t == 'down':#case 2
                    nextSeg = Segment(strokes[i:i+2],currentTrait['endIndex'])
                    preSeg.mature(currentSeg)
                    currentSeg.mature(nextSeg)
                    segs += [currentSeg,nextSeg]
                    resolveSeg(strokes[i+nextSeg.numOfStrokes:],segs,nextSeg)
                    break
    
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
            return Segment(strokes[:i+1])

    return None

def locateSimpleDown(strokes):
    g = strokes[0]['from'][1]
    d = strokes[0]['to'][1]
    prev = (strokes[0]['from'][1],strokes[0]['to'][1])
    for i in range(2,len(strokes),2):
        if strokes[i]['from'][1] > prev[0]: #break wrong end
            return None
        if strokes[i]['to'][1] < prev[1]:            
            return Segment(strokes[:i+1])

    return None

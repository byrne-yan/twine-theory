class Stroke:
    def __init__(self,kseq,begin,end):
        assert(begin<len(kseq))
        assert(end<=len(kseq))
        if end-begin<=4:
            import pdb;pdb.set_trace()
        assert(end-begin>4)
        self._kseq = kseq
        self._begin = begin
        self._end = end
        
        self.direction = 'up' if kseq[end-1]['high'] > kseq[begin]['high'] else 'down'
        self.status = 'growing'

        self._trick = {}
    def __str__(self):
        return "%f(%s) ==%s=> %f(%s): %s" % (\
            self._kseq[self._begin]['low'] if self.direction=='up' else self._kseq[self._begin]['high'],
            self._kseq[self._begin]['time'] ,
            self.direction,
            self._kseq[self._end-1]['high'] if self.direction=='up' else self._kseq[self._end-1]['low'],
            self._kseq[self._end-1]['time'],
            self.status            
            )

    def to_dict(self):
        return {"from":(self._begin,self._kseq[self._begin]['low'] if self.direction=='up' else self._kseq[self._begin]['high']),
                "to":(self._end-1,self._kseq[self._end-1]['high'] if self.direction=='up' else self._kseq[self._end-1]['low']),
                "isUp":self.direction=='up',
                "growing":self.status=='growing'
                }

    def changeIndex(self,kseq,start,end):
        self._kseq = kseq
        self._begin = start
        self._end = end

        
    def __repr__(self):
        return str(self)

    def mature(self,brokenBy):
        self.status = 'mature'
        self.brokenBy = brokenBy
        
    def grows(self,step):
        if self._end+step > len(self._kseq):
            import pdb;pdb.set_trace()
        assert(self._end+step<=len(self._kseq))
        self._end += step

    def __getattr__(self, attr):
        if attr == 'high':
            return self._kseq[self._end-1]['high'] if self.direction=='up' else self._kseq[self._begin]['high']
        elif attr == 'low':
            return self._kseq[self._begin]['low']  if self.direction=='up' else self._kseq[self._end-1]['low'] 
        elif attr == 'lastK':
            return self._kseq[self._end-1]
        elif attr == 'isUp':
            return self.direction=='up'
        elif attr == 'size':
            return self._end-self._begin
        elif attr == 'begin':
            return self._begin
        elif attr == 'end':
            return self._end

    def __setitem__(self,name,value):
        if name == 'hops':
            self._trick[name] = value
        return supper().__setitem__(index)

    def __contains__(self, index):
        if index == 'isUp'or index == 'from' or index == 'to' or index == 'growing':
           return True
        elif index == 'hops':
            return index in self._trick
        return False
    
    def __getitem__(self,index):
        if index == 'isUp':
            return self.direction=='up'
        elif index == 'from':
            return (self._begin,self._kseq[self._begin]['low'] if self.direction=='up' else self._kseq[self._begin]['high'])
        elif index == 'to':
            return (self._end-1,self._kseq[self._end-1]['high'] if self.direction=='up' else self._kseq[self._end-1]['low'])
        elif index == 'growing':
            return self.status == 'growing'
        elif index == 'hops':
            return self._trick[index] if index in self._trick else None
        #return supper().__getitem__(index)
        
def resolve_strokes(kseq,begin,end,strokes,currentStroke=None,prevStroke=None):
    assert(len(kseq)>=begin)
    if currentStroke is None:
        if end-begin<5:
            return
        #locate fitst consucutive 5 monotous Ks
        
        mono = {'direction':'up','from':begin,'count':1}
        lastK = kseq[begin]
        for i in range(begin+1,end):
            currentK = kseq[i]
            if currentK['high'] > lastK['high']:
               if mono['direction'] == 'up':
                   mono['count'] += 1
                   if mono['count'] == 5:
                       nextStroke = Stroke(kseq,mono['from'],i+1)
                       strokes.append(nextStroke)
                       return resolve_strokes(kseq,i,end,strokes,nextStroke)
                   lastK = currentK
               else:
                   mono = {'direction':'up','from':i-1,'count':2}
                   lastK = currentK
            else:
               if mono['direction'] == 'down':
                   mono['count'] += 1
                   if mono['count'] == 5:
                       nextStroke = Stroke(kseq,mono['from'],i+1)
                       strokes.append(nextStroke)
                       return resolve_strokes(kseq,i,end,strokes,nextStroke)
                   lastK = currentK 
               else:
                   mono = {'direction':'down','from':i-1,'count':2}
                   lastK = currentK
    else:
        assert(begin+1 >= currentStroke._end)

##        import pdb;pdb.set_trace()
        if currentStroke.direction=='up':
            lastK = currentStroke.lastK
            lastPeak = begin
            noDown = False
            for i in range(begin+1,end):
               currentK = kseq[i]
               if currentK['high'] > currentStroke.lastK['high']:#stroke continues
                   currentStroke.grows(i-lastPeak)
                   lastPeak = i
                   lastK = currentK
                   noDown = False
               else: #top candidates
                   if not noDown:
                        nextStroke = testStroke(kseq,i-1,end,'down')
                        if nextStroke:
                            currentStroke.mature(nextStroke)
                            strokes.append(nextStroke)
                            return resolve_strokes(kseq,i+nextStroke.size-2,end,strokes,nextStroke,currentStroke)
                        else:
                            if prevStroke:
                                nextStroke = testStroke2(kseq,i-1,end,'down',prevStroke.lastK['low'])
                                if nextStroke:
                                    prevStroke.grows(nextStroke.begin-currentStroke.begin);
                                    prevStroke.mature(nextStroke)
                                    strokes.remove(currentStroke)
                                    strokes.append(nextStroke)
                                    return resolve_strokes(kseq,nextStroke.end-1,end,strokes,nextStroke,prevStroke)
                                else:
                                    noDown = True
                            else:
                                noDown = True
        else:#down
            lastK = currentStroke.lastK
            lastPeak = begin
            noUp = False
            for i in range(begin+1,end):
                currentK = kseq[i]
                if currentK['low'] < currentStroke.lastK['low']:#stroke continues
                    currentStroke.grows(i-lastPeak)
                    lastPeak = i
                    lastK = currentK
                    noUp = False
                else: #bottom condidates
                    if not noUp:
                        nextStroke = testStroke(kseq,i-1,end,'up')
                        if nextStroke :  #bottom
                            currentStroke.mature(nextStroke)
                            strokes.append(nextStroke)
                            return resolve_strokes(kseq,i+nextStroke.size-2,end,strokes,nextStroke,currentStroke)
                        else:
                            if prevStroke:
                                nextStroke = testStroke2(kseq,i-1,end,'up',prevStroke.lastK['high'])
                                if nextStroke:
                                    prevStroke.grows(nextStroke.begin-currentStroke.begin);
                                    prevStroke.mature(nextStroke)
                                    strokes.remove(currentStroke)
                                    strokes.append(nextStroke)
                                    return resolve_strokes(kseq,nextStroke.end-1,end,strokes,nextStroke,prevStroke)
                                else:
                                    noUp= True
                            else:
                                noUp= True
                        
                        
        
def testStroke(kseq,begin,end,direction):
    if end-begin < 5:
        return
    if direction == 'up':
        base = kseq[begin]['low']
        lastK = kseq[begin]
        count = 1
        for i in range(begin+1,end):
            currentK = kseq[i]
            count += 1
            if currentK['high'] > lastK['high']:
                if count >= 5:
                    return Stroke(kseq,begin,i+1)
                lastK = currentK
            if currentK['low'] < base:
                return
    else:
        base = kseq[begin]['high']
        lastK = kseq[begin]
        count = 1
        for i in range(begin+1,end):
            currentK = kseq[i]
            count += 1
            if currentK['low'] < lastK['low']:
                if count >= 5:
                    return Stroke(kseq,begin,i+1)
                lastK = currentK
            if currentK['high'] > base:
                return
def testStroke2(kseq,begin,end,direction,prevStrokePeak):
    if direction == 'up':
        for i in range(begin+1,min(end,begin+4)):
            currentK = kseq[i]
            
            if currentK['high'] > prevStrokePeak:
                nextStroke = testStroke(kseq,i,end,'down')
                if nextStroke:
                    return nextStroke
    else:
        for i in range(begin+1,min(end,begin+4)):
            currentK = kseq[i]
            if currentK['low'] < prevStrokePeak:
                nextStroke = testStroke(kseq,i,end,'up')
                if nextStroke:
                    return nextStroke

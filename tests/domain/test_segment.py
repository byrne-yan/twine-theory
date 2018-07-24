from twine_theory.domain import twine_theory as twine

class fakeStroke:
    def __init__(self,stroke_dict):
        self._stroke = stroke_dict
    def __setitem__(self,key,value):
        if key=="hops":
            self._stroke[key] = value
        else:
            super().__setitem__(key)
            
    def __getitem__(self,key):
        if key=="hops":
            if key in self._stroke:
                return self._stroke[key]
            else:
                raise KeyError
        else:
            return self._stroke[key]
    def __contains__(self, item):
        return item in self._stroke
    
##    def __setattr__(self,name,value):
##        if name=="hops":
##            self._hops = value
##            self._flag = True
##        else:
##            super().__setattr__(name, value)
##            
##    def __getattr__(self,key):
##        if key=="hops":
##            return self._hops if self._flag else None
##        super().__getattr__(key)
            
    def to_dict(self):
        return self

#standard situation a
   
##               8 
##               /\
##              /  \    6
##        5    /    \  /\
##        /\  /      \/  \
##       /  \/       4    \
##      /   3              \
##     /                   2
##    1

def test_seg_split_a():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,1),'to':(2,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,5),'to':(4,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,3),'to':(6,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,8),'to':(8,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(8,4),'to':(10,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(10,6),'to':(12,2),'isUp':False,'growing':False})
        ]
    s.makeupSegment()

    assert(2 == len(s._segment))

    assert(eval(str(s._segment[0])) == {
        'from': (0,1),
        'to': (6,8),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (6,8),
        'to': (12,2),
        'isUp': False,
        'bi': [3,4,5],
        'growing':True
        })
    assert(s._segment[0]['from']==(0,1))
    assert(s._segment[0]['to']==(6,8))
    assert(s._segment[0]['growing']==False)
    assert(s._segment[1]['growing']==True)

#standard situation a
   
##                             8
##                             /\ 7
##             6           6  /  \/\ 
##        5    /\       5  /\/   6  \
##        /\  /  \   4  /\/ 5        \
##       /  \/    \  /\/ 4           4
##      /   3      \/ 3     
##     /           2       
##    1

def test_seg_split_a2():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,1),'to':(2,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,5),'to':(4,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,3),'to':(6,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,6),'to':(8,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(8,2),'to':(10,4),'isUp':True,'growing':False}),
        fakeStroke({'from':(10,4),'to':(12,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(12,3),'to':(14,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(14,5),'to':(16,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(16,4),'to':(18,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(18,6),'to':(20,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(20,5),'to':(22,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(22,8),'to':(24,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(24,6),'to':(26,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(26,7),'to':(28,4),'isUp':False,'growing':False})
        ]
    s.makeupSegment()

    assert(2 == len(s._segment))

    assert(eval(str(s._segment[0])) == {
        'from': (0,1),
        'to': (22,8),
        'isUp': True,
        'bi': [0,1,2,3,4,5,6,7,8,9,10],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (22,8),
        'to': (28,4),
        'isUp': False,
        'bi': [11,12,13],
        'growing':True
        })

#standard situation quekou-a

##                9
##                /\   8       8 
##               /  \  /\   7  /
##              /    \/  \  /\/
##             /     6    \/ 6
##       4    /           5  
##       /\  /                 
##      /  \/              
##     /   2                
##    1

def test_seg_split_qk_a():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,1),'to':(2,4),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,4),'to':(4,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,2),'to':(6,9),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,9),'to':(8,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(8,6),'to':(10,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(10,8),'to':(12,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(12,5),'to':(14,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(14,7),'to':(16,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(16,6),'to':(18,8),'isUp':True,'growing':False}),
        ]
    s.makeupSegment()
    assert(3 == len(s._segment))

    assert(eval(str(s._segment[0])) == {
        'from': (0,1),
        'to': (6,9),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (6,9),
        'to': (12,5),
        'isUp': False,
        'bi': [3,4,5],
        'growing':False
        })
    assert(eval(str(s._segment[2])) == {
        'from': (12,5),
        'to': (18,8),
        'isUp': True,
        'bi': [6,7,8],
        'growing':True
        })

#standard situation b

##             8 
##             /\
##            /  \      6
##        5  /    \    /\
##        /\/      \  /  \
##       / 4        \/    \
##      /           3      \
##     /                   2
##    1
def test_seg_split_b():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,1),'to':(1,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(1,5),'to':(2,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(2,4),'to':(3,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(3,8),'to':(4,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,3),'to':(5,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(5,6),'to':(6,2),'isUp':False,'growing':False}),
        ]
    s.makeupSegment()
    
    assert(2 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,1),
        'to': (3,8),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,8),
        'to': (6,2),
        'isUp': False,
        'bi': [3,4,5],
        'growing':True
        })

#standard situation quekou b

##             8 
##             /\ 7          7
##            /  \/\        /
##        5  /   6  \   5  /
##        /\/        \  /\/
##       / 4          \/ 4   
##      /             3    
##     /                   
##    1
def test_seg_split_qk_b():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,1),'to':(1,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(1,5),'to':(2,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(2,4),'to':(3,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(3,8),'to':(4,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,6),'to':(5,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(5,7),'to':(6,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(6,3),'to':(7,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(7,5),'to':(8,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(8,4),'to':(9,7),'isUp':True,'growing':False})
        ]
    s.makeupSegment()
    
    assert(3 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,1),
        'to': (3,8),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,8),
        'to': (6,3),
        'isUp': False,
        'bi': [3,4,5],
        'growing':False
        })
    assert(eval(str(s._segment[2])) == {
        'from': (6,3),
        'to': (9,7),
        'isUp': True,
        'bi': [6,7,8],
        'growing':True
        })


#standard situation c
##                            9
##             8              /
##             /\            / 
##            /  \     6    / 
##        5  /    \    /\  /  
##        /\/      \  /  \/   
##       / 4        \/   4 
##      /           3     
##     /                  
##    1
def test_seg_split_c():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,1),'to':(2,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,5),'to':(4,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,4),'to':(6,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,8),'to':(8,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(8,3),'to':(10,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(10,6),'to':(12,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(12,4),'to':(14,9),'isUp':False,'growing':False})
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,1),
        'to': (14,9),
        'isUp': True,
        'bi': [0,1,2,3,4,5,6],
        'growing':True
        })

#standard situation quekou c
##                         9
##               8        /       
##               /\   7  /
##              /  \  /\/
##             /    \/ 6 
##       4    /     5      
##       /\  /                 
##      /  \/              
##     /   2                
##    1
def test_seg_split_qk_c():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,1),'to':(2,4),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,4),'to':(4,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,2),'to':(6,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,8),'to':(8,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(8,5),'to':(10,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(10,7),'to':(12,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(12,6),'to':(14,9),'isUp':True,'growing':False})
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,1),
        'to': (14,9),
        'isUp': True,
        'bi': [0,1,2,3,4,5,6],
        'growing':True
        })
    
#standard situation d
##                            
##             8              
##             /\           7 
##            /  \     6    /\ 
##        5  /    \    /\  /  \
##        /\/      \  /  \/    \
##       / 4        \/   4      \
##      /           3            \
##     /                         2
##    1
def test_seg_split_d():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,1),'to':(3,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(3,5),'to':(6,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(6,4),'to':(9,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(9,8),'to':(12,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(12,3),'to':(15,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(15,6),'to':(18,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(18,4),'to':(21,7),'isUp':False,'growing':False}),
        fakeStroke({'from':(21,7),'to':(24,2),'isUp':False,'growing':False})
        ]
    s.makeupSegment()
    
    assert(2 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,1),
        'to': (9,8),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (9,8),
        'to': (24,2),
        'isUp': False,
        'bi': [3,4,5,6,7],
        'growing':True
        })
#standard situation quekou d
##                9         
##                /\       8        
##               /  \   7  /\ 
##              /    \  /\/  \
##             /      \/ 6    \
##            /       5        \
##        3  /                 4  
##        /\/              
##       / 2                
##      1
def test_seg_split_qk_d():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,1),'to':(1,3),'isUp':True,'growing':False}),
        fakeStroke({'from':(1,3),'to':(2,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(2,2),'to':(3,9),'isUp':True,'growing':False}),
        fakeStroke({'from':(3,9),'to':(4,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,5),'to':(5,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(5,7),'to':(6,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(6,6),'to':(7,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(7,8),'to':(8,4),'isUp':False,'growing':False})
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,1),
        'to': (3,9),
        'isUp': True,
        'bi': [0,1,2],
        'growing':True
        })

#standard situation e
##                                         12
##                                         /\   11
##                                        /  \  /\   10
##                          9            /    \/  \  /\
##               8          /\          /     9    \/  \
##               /\        /  \        /           8    \
##              /  \      /    \ 7    /                 7
##             /    \    /      \/\  /
##            /      \  /       6  \/
##           /        \/           5
##          /         4                  
##         3            
##                        
def test_seg_split_e():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,3),'to':(1,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(1,8),'to':(2,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(2,4),'to':(3,9),'isUp':True,'growing':False}),
        fakeStroke({'from':(3,9),'to':(4,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,6),'to':(5,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(5,7),'to':(6,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(6,5),'to':(7,12),'isUp':True,'growing':False}),
        fakeStroke({'from':(7,12),'to':(8,9),'isUp':False,'growing':False}),
        fakeStroke({'from':(8,9),'to':(9,11),'isUp':True,'growing':False}),
        fakeStroke({'from':(9,11),'to':(10,8),'isUp':False,'growing':False}),
        fakeStroke({'from':(10,8),'to':(11,10),'isUp':True,'growing':False}),
        fakeStroke({'from':(11,10),'to':(12,7),'isUp':False,'growing':False})
        
        ]
    s.makeupSegment()
    
    assert(4 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,3),
        'to': (3,9),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,9),
        'to': (6,5),
        'isUp': False,
        'bi': [3,4,5],
        'growing':False
        })
    assert(eval(str(s._segment[2])) == {
        'from': (6,5),
        'to': (9,11),
        'isUp': True,
        'bi': [6,7,8],
        'growing':False
        })
    assert(eval(str(s._segment[3])) == {
        'from': (9,11),
        'to': (12,7),
        'isUp': False,
        'bi': [9,10,11],
        'growing':True
        })

#standard situation quekou e
##                                         12
##                    11                   /
##                    /\             10   /
##                   /  \   9        /\  /  
##                  /    \  /\      /  \/      
##                 /      \/  \    /   8   
##                /       7    \  /      
##               /              \/    
##           4  /               5
##           /\/         
##          / 3                 
##         2            
##                     
def test_seg_split_qk_e():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,2),'to':(1,4),'isUp':True,'growing':False}),
        fakeStroke({'from':(1,4),'to':(2,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(2,3),'to':(3,11),'isUp':True,'growing':False}),
        fakeStroke({'from':(3,11),'to':(4,7),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,7),'to':(5,9),'isUp':True,'growing':False}),
        fakeStroke({'from':(5,9),'to':(6,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(6,5),'to':(7,10),'isUp':True,'growing':False}),
        fakeStroke({'from':(7,10),'to':(8,8),'isUp':False,'growing':False}),
        fakeStroke({'from':(8,8),'to':(9,12),'isUp':True,'growing':False})
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,2),
        'to': (9,12),
        'isUp': True,
        'bi': [0,1,2,3,4,5,6,7,8],
        'growing':True
        })

#standard situation f
##                               
##                                      11
##                             10       / 
##                  9          /\      /  
##         8        /\        /  \    /   
##         /\      /  \ 7    /    \  /  
##        /  \    /    \/\  /      \/   
##       /    \  /     6  \/       6
##      /      \/         5
##     /       4         
##    3                
##                     
##                     
def test_seg_split_f():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,3),'to':(1,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(1,8),'to':(2,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(2,4),'to':(3,9),'isUp':True,'growing':False}),
        fakeStroke({'from':(3,9),'to':(4,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,6),'to':(5,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(5,7),'to':(6,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(6,5),'to':(7,10),'isUp':True,'growing':False}),
        fakeStroke({'from':(7,10),'to':(8,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(8,6),'to':(9,11),'isUp':True,'growing':False})     
        ]
    s.makeupSegment()
    
    assert(3 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,3),
        'to': (3,9),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,9),
        'to': (6,5),
        'isUp': False,
        'bi': [3,4,5],
        'growing':False
        })
    assert(eval(str(s._segment[2])) == {
        'from': (6,5),
        'to': (9,11),
        'isUp': True,
        'bi': [6,7,8],
        'growing':True
        })
    
#standard situation quekou f
##                               10      
##                            9  /
##               8            /\/       
##               /\   7      / 8
##              /  \  /\    /
##             /    \/  \  / 
##            /     5    \/   
##        3  /           4      
##        /\/              
##       / 2                
##      1
def test_seg_split_qk_f():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,1),'to':(1,3),'isUp':True,'growing':False}),
        fakeStroke({'from':(1,3),'to':(2,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(2,2),'to':(3,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(3,8),'to':(4,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(4,5),'to':(5,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(5,7),'to':(6,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(6,4),'to':(7,9),'isUp':True,'growing':False}),
        fakeStroke({'from':(7,9),'to':(8,8),'isUp':False,'growing':False}),
        fakeStroke({'from':(8,8),'to':(9,10),'isUp':True,'growing':False})
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,1),
        'to': (9,10),
        'isUp': True,
        'bi': [0,1,2,3,4,5,6,7,8],
        'growing':True
        })    

########  down ######
    
#standard down situation a
   
##  8 
##   \                   7
##    \   6              /
##     \  /\       5    /
##      \/  \      /\  /
##      4    \    /  \/
##            \  /   3
##             \/  
##             1

def test_seg_split_xdown_a():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,8),'to':(1,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,4),'to':(2,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,6),'to':(3,1),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,1),'to':(4,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,5),'to':(5,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,3),'to':(6,7),'isUp':True,'growing':False}),
        ]
    s.makeupSegment()
    assert(2 == len(s._segment))

    assert(eval(str(s._segment[0])) == {
        'from': (0,8),
        'to': (3,1),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,1),
        'to': (6,7),
        'isUp': True,
        'bi': [3,4,5],
        'growing':True
        })

#standard down situation quekou-a

##    9
##     \   8
##      \  /\
##       \/  \           5
##       6    \     4    /\ 4
##             \    /\  /  \/\
##              \  /  \/   3  \
##               \/   2       2
##               1
##    

def test_seg_split_xdown_qk_a():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,9),'to':(1,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,6),'to':(2,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,8),'to':(3,1),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,1),'to':(4,4),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,4),'to':(5,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,2),'to':(6,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,5),'to':(7,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(7,3),'to':(8,4),'isUp':True,'growing':False}),
        fakeStroke({'from':(8,4),'to':(9,2),'isUp':False,'growing':False}),
        ]
    s.makeupSegment()
    assert(3 == len(s._segment))

    assert(eval(str(s._segment[0])) == {
        'from': (0,9),
        'to': (3,1),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,1),
        'to': (6,5),
        'isUp': True,
        'bi': [3,4,5],
        'growing':False
        })
    assert(eval(str(s._segment[2])) == {
        'from': (6,5),
        'to': (9,2),
        'isUp': False,
        'bi': [6,7,8],
        'growing':True
        })

#standard down situation b


##    9
##     \                   8
##      \           7      /
##       \ 6        /\    /
##        \/\      /  \  /
##        5  \    /    \/
##            \  /     4
##             \/
##             2
    
def test_seg_split_xdown_b():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,9),'to':(1,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,5),'to':(2,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,6),'to':(3,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,2),'to':(4,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,7),'to':(5,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,4),'to':(6,8),'isUp':True,'growing':False})
        ]
    s.makeupSegment()
    
    assert(2 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,9),
        'to': (3,2),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,2),
        'to': (6,8),
        'isUp': True,
        'bi': [3,4,5],
        'growing':True
        })

#standard down situation quekou b

##    9
##     \      
##      \             7
##       \ 6          /\ 6
##        \/\        /  \/\
##        5  \   4  /   5  \
##            \  /\/        \
##             \/ 3         3
##             2
def test_seg_split_xdown_qk_b():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,9),'to':(1,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,5),'to':(2,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,6),'to':(3,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,2),'to':(4,4),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,4),'to':(5,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,3),'to':(6,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,7),'to':(7,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(7,5),'to':(8,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(8,6),'to':(9,3),'isUp':False,'growing':False})
        ]
    s.makeupSegment()
    
    assert(3 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,9),
        'to': (3,2),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,2),
        'to': (6,7),
        'isUp': True,
        'bi': [3,4,5],
        'growing':False
        })
    assert(eval(str(s._segment[2])) == {
        'from': (6,7),
        'to': (9,3),
        'isUp': False,
        'bi': [6,7,8],
        'growing':True
        })


#standard down situation c

##    9
##     \
##      \           7
##       \ 6        /\   6
##        \/\      /  \  /\
##        5  \    /    \/  \
##            \  /     4    \
##             \/            \
##             2              \
##                            1
def test_seg_split_xdown_c():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,9),'to':(1,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,5),'to':(2,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,6),'to':(3,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,2),'to':(4,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,7),'to':(5,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,4),'to':(6,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,6),'to':(7,1),'isUp':False,'growing':False})
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,9),
        'to': (7,1),
        'isUp': False,
        'bi': [0,1,2,3,4,5,6],
        'growing':True
        })

#standard down situation quekou c
##    9   
##     \   8
##      \  /\
##       \/  \
##       6    \     5
##             \    /\ 4
##              \  /  \/\
##               \/   3  \
##               2        \
##                         1
def test_seg_split_xdown_qk_c():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,9),'to':(1,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,6),'to':(2,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,8),'to':(3,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,2),'to':(4,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,5),'to':(5,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,3),'to':(6,4),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,4),'to':(7,1),'isUp':False,'growing':False})
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,9),
        'to': (7,1),
        'isUp': False,
        'bi': [0,1,2,3,4,5,6],
        'growing':True
        })
    
#standard down situation d
##    9                        
##     \                         8 
##      \           7            /
##       \ 6        /\   6      /
##        \/\      /  \  /\    /
##        5  \    /    \/  \  /
##            \  /     4    \/
##             \/           3 
##             2
##    
def test_seg_split_xdown_d():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,9),'to':(1,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,5),'to':(2,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,6),'to':(3,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,2),'to':(4,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,7),'to':(5,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,4),'to':(6,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,6),'to':(7,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(7,3),'to':(8,8),'isUp':True,'growing':False})
        ]
    s.makeupSegment()
    
    assert(2 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,9),
        'to': (3,2),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,2),
        'to': (8,8),
        'isUp': True,
        'bi': [3,4,5,6,7],
        'growing':True
        })
#standard down situation quekou d
##      9
##       \ 8
##        \/\
##        7  \                 6 
##            \       5        /  
##             \      /\ 4    /
##              \    /  \/\  /
##               \  /   3  \/
##                \/       2
##                1
def test_seg_split_xdown_qk_d():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,9),'to':(1,7),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,7),'to':(2,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,8),'to':(3,1),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,1),'to':(4,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,5),'to':(5,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,3),'to':(6,4),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,4),'to':(7,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(7,2),'to':(8,6),'isUp':True,'growing':False})
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,9),
        'to': (3,1),
        'isUp': False,
        'bi': [0,1,2],
        'growing':True
        })

#standard down situation e
##    10                 
##     \       9           
##      \      /\         8
##       \    /  \     7  /\
##        \  /    \    /\/  \                 6
##         \/      \  / 6    \           5    /
##         5        \/        \     4    /\  /
##                  4          \    /\  /  \/
##                              \  /  \/   3
##                               \/   2
##                               1  
##     
def test_seg_split_xdown_e():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,10),'to':(1,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,5),'to':(2,9),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,9),'to':(3,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,4),'to':(4,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,7),'to':(5,6),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,6),'to':(6,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,8),'to':(7,1),'isUp':False,'growing':False}),
        fakeStroke({'from':(7,1),'to':(8,4),'isUp':True,'growing':False}),
        fakeStroke({'from':(8,4),'to':(9,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(9,2),'to':(10,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(10,5),'to':(11,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(11,3),'to':(12,6),'isUp':True,'growing':False})
        
        ]
    s.makeupSegment()
    
    assert(4 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,10),
        'to': (3,4),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,4),
        'to': (6,8),
        'isUp': True,
        'bi': [3,4,5],
        'growing':False
        })
    assert(eval(str(s._segment[2])) == {
        'from': (6,8),
        'to': (9,2),
        'isUp': False,
        'bi': [6,7,8],
        'growing':False
        })
    assert(eval(str(s._segment[3])) == {
        'from': (9,2),
        'to': (12,6),
        'isUp': True,
        'bi': [9,10,11],
        'growing':True
        })

#standard down situation quekou e
##         11
##          \ 10
##           \/\
##           9  \               8
##               \              /\
##                \       6    /  \
##                 \      /\  /    \   5
##                  \    /  \/      \  /\
##                   \  /   4        \/  \
##                    \/             3    \
##                    2                    \
##                                         1  
##         
##      
def test_seg_split_xdown_qk_e():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,11),'to':(1,9),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,9),'to':(2,10),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,10),'to':(3,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,2),'to':(4,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,6),'to':(5,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,4),'to':(6,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,8),'to':(7,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(7,3),'to':(8,5),'isUp':True,'growing':False}),
        fakeStroke({'from':(8,5),'to':(9,1),'isUp':False,'growing':False})
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,11),
        'to': (9,1),
        'isUp': False,
        'bi': [0,1,2,3,4,5,6,7,8],
        'growing':True
        })

#standard down situation f
##    9 
##     \       8
##      \      /\         7
##       \    /  \     6  /\       6 
##        \  /    \    /\/  \      /\
##         \/      \  / 5    \    /  \
##         4        \/        \  /    \
##                  3          \/      \
##                             2        \
##                                      1
##   
def test_seg_split_xdown_f():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,9),'to':(1,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,4),'to':(2,8),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,8),'to':(3,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,3),'to':(4,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,6),'to':(5,5),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,5),'to':(6,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,7),'to':(7,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(7,2),'to':(8,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(8,6),'to':(9,1),'isUp':False,'growing':False})      
        ]
    s.makeupSegment()
    
    assert(3 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,9),
        'to': (3,3),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(eval(str(s._segment[1])) == {
        'from': (3,3),
        'to': (6,7),
        'isUp': True,
        'bi': [3,4,5],
        'growing':False
        })
    assert(eval(str(s._segment[2])) == {
        'from': (6,7),
        'to': (9,1),
        'isUp': False,
        'bi': [6,7,8],
        'growing':True
        })
    
#standard down situation quekou f
##      10
##       \ 9
##        \/\
##        8  \           7
##            \     6    /\
##             \    /\  /  \
##              \  /  \/    \
##               \/   4      \ 3 
##               3            \/\
##                            2  \ 
##                               1
def test_seg_split_xdown_qk_f():
    s = twine.KSeq('day',[])
    s._strokes = [
        fakeStroke({'from':(0,10),'to':(1,8),'isUp':False,'growing':False}),
        fakeStroke({'from':(1,8),'to':(2,9),'isUp':True,'growing':False}),
        fakeStroke({'from':(2,9),'to':(3,3),'isUp':False,'growing':False}),
        fakeStroke({'from':(3,3),'to':(4,6),'isUp':True,'growing':False}),
        fakeStroke({'from':(4,6),'to':(5,4),'isUp':False,'growing':False}),
        fakeStroke({'from':(5,4),'to':(6,7),'isUp':True,'growing':False}),
        fakeStroke({'from':(6,7),'to':(7,2),'isUp':False,'growing':False}),
        fakeStroke({'from':(7,2),'to':(8,3),'isUp':True,'growing':False}),
        fakeStroke({'from':(8,3),'to':(9,1),'isUp':False,'growing':False})
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(eval(str(s._segment[0])) == {
        'from': (0,10),
        'to': (9,1),
        'isUp': False,
        'bi': [0,1,2,3,4,5,6,7,8],
        'growing':True
        })    


    
def test_seg_split_compound_1():
    import pandas as pd
    df = pd.read_csv('./tests/fixtures/000002_30m_stroke.csv',header=0,names=['date','stroke'])
    s = twine.KSeq('30m',[])
    s._strokes = []
    t0 = None
    for t in df.itertuples():
        if t0 is not None:
            up = True if t.stroke>t0.stroke else False
            s._strokes.append(fakeStroke({
                'from':(t0.Index,t0.stroke),
                'to':(t.Index,t.stroke),
                'isUp':up,
                'growing':False}))
        t0 = t

    

    s.makeupSegment()
    assert(6 == len(s._segment))
        
def test_seg_split_compound_2():
    import pandas as pd
    df = pd.read_csv('./tests/fixtures/002628_w_stroke.csv',header=0,names=['date','stroke'])
    s = twine.KSeq('30m',[])
    s._strokes = []
    t0 = None
    for t in df.itertuples():
        if t0 is not None:
            up = True if t.stroke>t0.stroke else False
            s._strokes.append(fakeStroke({
                'from':(t0.Index,t0.stroke),
                'to':(t.Index,t.stroke),
                'isUp':up,
                'growing':False}))
        t0 = t

    

    s.makeupSegment()
    assert(4 == len(s._segment))
    

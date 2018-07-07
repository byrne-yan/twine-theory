from twine_theory.domain import twine_theory as twine

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
    s._bi = [
        {'from':(0,1),'to':(1,5),'isUp':True,'growing':False},
        {'from':(1,5),'to':(2,3),'isUp':False,'growing':False},
        {'from':(2,3),'to':(3,8),'isUp':True,'growing':False},
        {'from':(3,8),'to':(4,4),'isUp':False,'growing':False},
        {'from':(4,4),'to':(5,6),'isUp':True,'growing':False},
        {'from':(5,6),'to':(6,2),'isUp':False,'growing':False},
        ]
    s.makeupSegment()
    assert(2 == len(s._segment))

    assert(s._segment[0] == {
        'from': (0,1),
        'to': (3,8),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
        'from': (3,8),
        'to': (6,2),
        'isUp': False,
        'bi': [3,4,5],
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
    s._bi = [
        {'from':(0,1),'to':(1,4),'isUp':True,'growing':False},
        {'from':(1,4),'to':(2,2),'isUp':False,'growing':False},
        {'from':(2,2),'to':(3,9),'isUp':True,'growing':False},
        {'from':(3,9),'to':(4,6),'isUp':False,'growing':False},
        {'from':(4,6),'to':(5,8),'isUp':True,'growing':False},
        {'from':(5,8),'to':(6,5),'isUp':False,'growing':False},
        {'from':(6,5),'to':(7,7),'isUp':True,'growing':False},
        {'from':(7,7),'to':(8,6),'isUp':False,'growing':False},
        {'from':(8,6),'to':(9,8),'isUp':True,'growing':False},
        ]
    s.makeupSegment()
    assert(3 == len(s._segment))

    assert(s._segment[0] == {
        'from': (0,1),
        'to': (3,9),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
        'from': (3,9),
        'to': (6,5),
        'isUp': False,
        'bi': [3,4,5],
        'growing':False
        })
    assert(s._segment[2] == {
        'from': (6,5),
        'to': (9,8),
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
    s._bi = [
        {'from':(0,1),'to':(1,5),'isUp':True,'growing':False},
        {'from':(1,5),'to':(2,4),'isUp':False,'growing':False},
        {'from':(2,4),'to':(3,8),'isUp':True,'growing':False},
        {'from':(3,8),'to':(4,3),'isUp':False,'growing':False},
        {'from':(4,3),'to':(5,6),'isUp':True,'growing':False},
        {'from':(5,6),'to':(6,2),'isUp':False,'growing':False},
        ]
    s.makeupSegment()
    
    assert(2 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,1),
        'to': (3,8),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
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
    s._bi = [
        {'from':(0,1),'to':(1,5),'isUp':True,'growing':False},
        {'from':(1,5),'to':(2,4),'isUp':False,'growing':False},
        {'from':(2,4),'to':(3,8),'isUp':True,'growing':False},
        {'from':(3,8),'to':(4,6),'isUp':False,'growing':False},
        {'from':(4,6),'to':(5,7),'isUp':True,'growing':False},
        {'from':(5,7),'to':(6,3),'isUp':False,'growing':False},
        {'from':(6,3),'to':(7,5),'isUp':True,'growing':False},
        {'from':(7,5),'to':(8,4),'isUp':False,'growing':False},
        {'from':(8,4),'to':(9,7),'isUp':True,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,1),
        'to': (3,8),
        'isUp': True,
        'bi': [0,1,2],
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
    s._bi = [
        {'from':(0,1),'to':(1,5),'isUp':True,'growing':False},
        {'from':(1,5),'to':(2,4),'isUp':False,'growing':False},
        {'from':(2,4),'to':(3,8),'isUp':True,'growing':False},
        {'from':(3,8),'to':(4,3),'isUp':False,'growing':False},
        {'from':(4,3),'to':(5,6),'isUp':True,'growing':False},
        {'from':(5,6),'to':(6,4),'isUp':False,'growing':False},
        {'from':(6,4),'to':(7,9),'isUp':False,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,1),
        'to': (7,9),
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
    s._bi = [
        {'from':(0,1),'to':(1,4),'isUp':True,'growing':False},
        {'from':(1,4),'to':(2,2),'isUp':False,'growing':False},
        {'from':(2,2),'to':(3,8),'isUp':True,'growing':False},
        {'from':(3,8),'to':(4,5),'isUp':False,'growing':False},
        {'from':(4,5),'to':(5,7),'isUp':True,'growing':False},
        {'from':(5,7),'to':(6,6),'isUp':False,'growing':False},
        {'from':(6,6),'to':(7,9),'isUp':True,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,1),
        'to': (7,9),
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
    s._bi = [
        {'from':(0,1),'to':(1,5),'isUp':True,'growing':False},
        {'from':(1,5),'to':(2,4),'isUp':False,'growing':False},
        {'from':(2,4),'to':(3,8),'isUp':True,'growing':False},
        {'from':(3,8),'to':(4,3),'isUp':False,'growing':False},
        {'from':(4,3),'to':(5,6),'isUp':True,'growing':False},
        {'from':(5,6),'to':(6,4),'isUp':False,'growing':False},
        {'from':(6,4),'to':(7,7),'isUp':False,'growing':False},
        {'from':(7,7),'to':(8,2),'isUp':False,'growing':False}
        ]
    s.makeupSegment()
    
    assert(2 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,1),
        'to': (3,8),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
        'from': (3,8),
        'to': (8,2),
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
    s._bi = [
        {'from':(0,1),'to':(1,3),'isUp':True,'growing':False},
        {'from':(1,3),'to':(2,2),'isUp':False,'growing':False},
        {'from':(2,2),'to':(3,9),'isUp':True,'growing':False},
        {'from':(3,9),'to':(4,5),'isUp':False,'growing':False},
        {'from':(4,5),'to':(5,7),'isUp':True,'growing':False},
        {'from':(5,7),'to':(6,6),'isUp':False,'growing':False},
        {'from':(6,6),'to':(7,8),'isUp':True,'growing':False},
        {'from':(7,8),'to':(8,4),'isUp':False,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,1),
        'to': (3,9),
        'isUp': True,
        'bi': [0,1,2],
        'growing':True
        })
                   
def test_seg_split_e():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,3),'to':(1,8),'isUp':True,'growing':False},
        {'from':(1,8),'to':(2,4),'isUp':False,'growing':False},
        {'from':(2,4),'to':(3,9),'isUp':True,'growing':False},
        {'from':(3,9),'to':(4,6),'isUp':False,'growing':False},
        {'from':(4,6),'to':(5,7),'isUp':True,'growing':False},
        {'from':(5,7),'to':(6,5),'isUp':False,'growing':False},
        {'from':(6,5),'to':(7,12),'isUp':True,'growing':False},
        {'from':(7,12),'to':(8,9),'isUp':False,'growing':False},
        {'from':(8,9),'to':(9,11),'isUp':True,'growing':False},
        {'from':(9,11),'to':(10,8),'isUp':False,'growing':False},
        {'from':(10,8),'to':(11,10),'isUp':True,'growing':False},
        {'from':(11,10),'to':(12,7),'isUp':False,'growing':False}
        
        ]
    s.makeupSegment()
    
    assert(4 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,3),
        'to': (3,9),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
        'from': (3,9),
        'to': (6,5),
        'isUp': False,
        'bi': [3,4,5],
        'growing':False
        })
    assert(s._segment[2] == {
        'from': (6,5),
        'to': (9,11),
        'isUp': True,
        'bi': [6,7,8],
        'growing':False
        })
    assert(s._segment[3] == {
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
    s._bi = [
        {'from':(0,2),'to':(1,4),'isUp':True,'growing':False},
        {'from':(1,4),'to':(2,3),'isUp':False,'growing':False},
        {'from':(2,3),'to':(3,11),'isUp':True,'growing':False},
        {'from':(3,11),'to':(4,7),'isUp':False,'growing':False},
        {'from':(4,7),'to':(5,9),'isUp':True,'growing':False},
        {'from':(5,9),'to':(6,5),'isUp':False,'growing':False},
        {'from':(6,5),'to':(7,10),'isUp':True,'growing':False},
        {'from':(7,10),'to':(8,8),'isUp':False,'growing':False},
        {'from':(8,8),'to':(9,12),'isUp':True,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
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
    s._bi = [
        {'from':(0,3),'to':(1,8),'isUp':True,'growing':False},
        {'from':(1,8),'to':(2,4),'isUp':False,'growing':False},
        {'from':(2,4),'to':(3,9),'isUp':True,'growing':False},
        {'from':(3,9),'to':(4,6),'isUp':False,'growing':False},
        {'from':(4,6),'to':(5,7),'isUp':True,'growing':False},
        {'from':(5,7),'to':(6,5),'isUp':False,'growing':False},
        {'from':(6,5),'to':(7,10),'isUp':True,'growing':False},
        {'from':(7,10),'to':(8,6),'isUp':False,'growing':False},
        {'from':(8,6),'to':(9,11),'isUp':True,'growing':False}        
        ]
    s.makeupSegment()
    
    assert(3 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,3),
        'to': (3,9),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
        'from': (3,9),
        'to': (6,5),
        'isUp': False,
        'bi': [3,4,5],
        'growing':False
        })
    assert(s._segment[2] == {
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
    s._bi = [
        {'from':(0,1),'to':(1,3),'isUp':True,'growing':False},
        {'from':(1,3),'to':(2,2),'isUp':False,'growing':False},
        {'from':(2,2),'to':(3,8),'isUp':True,'growing':False},
        {'from':(3,8),'to':(4,5),'isUp':False,'growing':False},
        {'from':(4,5),'to':(5,7),'isUp':True,'growing':False},
        {'from':(5,7),'to':(6,4),'isUp':False,'growing':False},
        {'from':(6,4),'to':(7,9),'isUp':True,'growing':False},
        {'from':(7,9),'to':(8,8),'isUp':False,'growing':False},
        {'from':(8,8),'to':(9,10),'isUp':True,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
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

def test_seg_split_down_a():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,8),'to':(1,4),'isUp':False,'growing':False},
        {'from':(1,4),'to':(2,6),'isUp':True,'growing':False},
        {'from':(2,6),'to':(3,1),'isUp':False,'growing':False},
        {'from':(3,1),'to':(4,5),'isUp':True,'growing':False},
        {'from':(4,5),'to':(5,3),'isUp':False,'growing':False},
        {'from':(5,3),'to':(6,7),'isUp':True,'growing':False},
        ]
    s.makeupSegment()
    assert(2 == len(s._segment))

    assert(s._segment[0] == {
        'from': (0,8),
        'to': (3,1),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
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

def test_seg_split_down_qk_a():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,9),'to':(1,6),'isUp':False,'growing':False},
        {'from':(1,6),'to':(2,8),'isUp':True,'growing':False},
        {'from':(2,8),'to':(3,1),'isUp':False,'growing':False},
        {'from':(3,1),'to':(4,4),'isUp':True,'growing':False},
        {'from':(4,4),'to':(5,2),'isUp':False,'growing':False},
        {'from':(5,2),'to':(6,5),'isUp':True,'growing':False},
        {'from':(6,5),'to':(7,3),'isUp':False,'growing':False},
        {'from':(7,3),'to':(8,4),'isUp':True,'growing':False},
        {'from':(8,4),'to':(9,2),'isUp':False,'growing':False},
        ]
    s.makeupSegment()
    assert(3 == len(s._segment))

    assert(s._segment[0] == {
        'from': (0,9),
        'to': (3,1),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
        'from': (3,1),
        'to': (6,5),
        'isUp': True,
        'bi': [3,4,5],
        'growing':False
        })
    assert(s._segment[2] == {
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
    
def test_seg_split_down_b():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,9),'to':(1,5),'isUp':False,'growing':False},
        {'from':(1,5),'to':(2,6),'isUp':True,'growing':False},
        {'from':(2,6),'to':(3,2),'isUp':False,'growing':False},
        {'from':(3,2),'to':(4,7),'isUp':True,'growing':False},
        {'from':(4,7),'to':(5,4),'isUp':False,'growing':False},
        {'from':(5,4),'to':(6,8),'isUp':True,'growing':False}
        ]
    s.makeupSegment()
    
    assert(2 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,9),
        'to': (3,2),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
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
def test_seg_split_down_qk_b():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,9),'to':(1,5),'isUp':False,'growing':False},
        {'from':(1,5),'to':(2,6),'isUp':True,'growing':False},
        {'from':(2,6),'to':(3,2),'isUp':False,'growing':False},
        {'from':(3,2),'to':(4,4),'isUp':True,'growing':False},
        {'from':(4,4),'to':(5,3),'isUp':False,'growing':False},
        {'from':(5,3),'to':(6,7),'isUp':True,'growing':False},
        {'from':(6,7),'to':(7,5),'isUp':False,'growing':False},
        {'from':(7,5),'to':(8,6),'isUp':True,'growing':False},
        {'from':(8,6),'to':(9,3),'isUp':False,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,9),
        'to': (3,2),
        'isUp': False,
        'bi': [0,1,2],
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
def test_seg_split_down_c():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,9),'to':(1,5),'isUp':False,'growing':False},
        {'from':(1,5),'to':(2,6),'isUp':True,'growing':False},
        {'from':(2,6),'to':(3,2),'isUp':False,'growing':False},
        {'from':(3,2),'to':(4,7),'isUp':True,'growing':False},
        {'from':(4,7),'to':(5,4),'isUp':False,'growing':False},
        {'from':(5,4),'to':(6,6),'isUp':True,'growing':False},
        {'from':(6,6),'to':(7,1),'isUp':False,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
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
def test_seg_split_down_qk_c():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,9),'to':(1,6),'isUp':False,'growing':False},
        {'from':(1,6),'to':(2,8),'isUp':True,'growing':False},
        {'from':(2,8),'to':(3,2),'isUp':False,'growing':False},
        {'from':(3,2),'to':(4,5),'isUp':True,'growing':False},
        {'from':(4,5),'to':(5,3),'isUp':False,'growing':False},
        {'from':(5,3),'to':(6,4),'isUp':True,'growing':False},
        {'from':(6,4),'to':(7,1),'isUp':False,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
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
def test_seg_split_down_d():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,9),'to':(1,5),'isUp':False,'growing':False},
        {'from':(1,5),'to':(2,6),'isUp':True,'growing':False},
        {'from':(2,6),'to':(3,2),'isUp':False,'growing':False},
        {'from':(3,2),'to':(4,7),'isUp':True,'growing':False},
        {'from':(4,7),'to':(5,4),'isUp':False,'growing':False},
        {'from':(5,4),'to':(6,4),'isUp':True,'growing':False},
        {'from':(6,6),'to':(7,3),'isUp':False,'growing':False},
        {'from':(7,3),'to':(8,8),'isUp':True,'growing':False}
        ]
    s.makeupSegment()
    
    assert(2 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,9),
        'to': (3,2),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
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
def test_seg_split_down_qk_d():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,9),'to':(1,7),'isUp':False,'growing':False},
        {'from':(1,7),'to':(2,8),'isUp':True,'growing':False},
        {'from':(2,8),'to':(3,1),'isUp':False,'growing':False},
        {'from':(3,1),'to':(4,5),'isUp':True,'growing':False},
        {'from':(4,5),'to':(5,3),'isUp':False,'growing':False},
        {'from':(5,3),'to':(6,4),'isUp':True,'growing':False},
        {'from':(6,4),'to':(7,2),'isUp':False,'growing':False},
        {'from':(7,2),'to':(8,6),'isUp':True,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
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
def test_seg_split_down_e():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,10),'to':(1,5),'isUp':False,'growing':False},
        {'from':(1,5),'to':(2,9),'isUp':True,'growing':False},
        {'from':(2,9),'to':(3,4),'isUp':False,'growing':False},
        {'from':(3,4),'to':(4,7),'isUp':True,'growing':False},
        {'from':(4,7),'to':(5,6),'isUp':False,'growing':False},
        {'from':(5,6),'to':(6,8),'isUp':True,'growing':False},
        {'from':(6,8),'to':(7,1),'isUp':False,'growing':False},
        {'from':(7,1),'to':(8,4),'isUp':True,'growing':False},
        {'from':(8,4),'to':(9,2),'isUp':False,'growing':False},
        {'from':(9,2),'to':(10,5),'isUp':True,'growing':False},
        {'from':(10,5),'to':(11,3),'isUp':False,'growing':False},
        {'from':(11,3),'to':(12,6),'isUp':True,'growing':False}
        
        ]
    s.makeupSegment()
    
    assert(4 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,10),
        'to': (3,4),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
        'from': (3,4),
        'to': (6,8),
        'isUp': True,
        'bi': [3,4,5],
        'growing':False
        })
    assert(s._segment[2] == {
        'from': (6,8),
        'to': (9,2),
        'isUp': False,
        'bi': [6,7,8],
        'growing':False
        })
    assert(s._segment[3] == {
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
def test_seg_split_down_qk_e():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,11),'to':(1,9),'isUp':False,'growing':False},
        {'from':(1,9),'to':(2,10),'isUp':True,'growing':False},
        {'from':(2,10),'to':(3,2),'isUp':False,'growing':False},
        {'from':(3,2),'to':(4,6),'isUp':True,'growing':False},
        {'from':(4,6),'to':(5,4),'isUp':False,'growing':False},
        {'from':(5,4),'to':(6,8),'isUp':True,'growing':False},
        {'from':(6,8),'to':(7,3),'isUp':False,'growing':False},
        {'from':(7,3),'to':(8,5),'isUp':True,'growing':False},
        {'from':(8,5),'to':(9,1),'isUp':False,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
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
def test_seg_split_down_f():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,9),'to':(1,4),'isUp':False,'growing':False},
        {'from':(1,4),'to':(2,8),'isUp':True,'growing':False},
        {'from':(2,8),'to':(3,3),'isUp':False,'growing':False},
        {'from':(3,3),'to':(4,6),'isUp':True,'growing':False},
        {'from':(4,6),'to':(5,5),'isUp':False,'growing':False},
        {'from':(5,5),'to':(6,7),'isUp':True,'growing':False},
        {'from':(6,7),'to':(7,2),'isUp':False,'growing':False},
        {'from':(7,2),'to':(8,6),'isUp':True,'growing':False},
        {'from':(8,6),'to':(9,1),'isUp':False,'growing':False}        
        ]
    s.makeupSegment()
    
    assert(3 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,9),
        'to': (3,3),
        'isUp': False,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
        'from': (3,3),
        'to': (6,7),
        'isUp': True,
        'bi': [3,4,5],
        'growing':False
        })
    assert(s._segment[2] == {
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
def test_seg_split_down_qk_f():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,10),'to':(1,8),'isUp':False,'growing':False},
        {'from':(1,8),'to':(2,9),'isUp':True,'growing':False},
        {'from':(2,9),'to':(3,3),'isUp':False,'growing':False},
        {'from':(3,3),'to':(4,6),'isUp':True,'growing':False},
        {'from':(4,6),'to':(5,4),'isUp':False,'growing':False},
        {'from':(5,4),'to':(6,7),'isUp':True,'growing':False},
        {'from':(6,7),'to':(7,2),'isUp':False,'growing':False},
        {'from':(7,2),'to':(8,3),'isUp':True,'growing':False},
        {'from':(8,3),'to':(9,1),'isUp':False,'growing':False}
        ]
    s.makeupSegment()
    
    assert(1 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,10),
        'to': (9,1),
        'isUp': False,
        'bi': [0,1,2,3,4,5,6,7,8],
        'growing':True
        })    


    

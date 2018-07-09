from twine_theory.domain import segments

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

def test_seg_resolve_a():
    
    strokes = [
        {'from':(0,1),'to':(1,5),'isUp':True,'growing':False},
        {'from':(1,5),'to':(2,3),'isUp':False,'growing':False},
        {'from':(2,3),'to':(3,8),'isUp':True,'growing':False},
        {'from':(3,8),'to':(4,4),'isUp':False,'growing':False},
        {'from':(4,4),'to':(5,6),'isUp':True,'growing':False},
        {'from':(5,6),'to':(6,2),'isUp':False,'growing':False}
        ]
    segs = segments.resolveSeg(strokes)
    
    assert(2 == len(segs))

    assert(segs[0] == {
        'from': (0,1),
        'to': (3,8),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(segs[1] == {
        'from': (3,8),
        'to': (6,2),
        'isUp': False,
        'bi': [3,4,5],
        'growing':True
        })

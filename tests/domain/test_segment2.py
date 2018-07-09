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
    segs = []
    segments.resolveSeg(strokes,segs)


    assert(2 == len(segs))

    assert(segs[0]._strokes[0] == strokes[0])
    assert(segs[0]._strokes[1] == strokes[1])
    assert(segs[0]._strokes[2] == strokes[2])
    assert(segs[0].direction == 'up')
    assert(segs[0].status == 'mature')

    assert(segs[1]._strokes[0] == strokes[3])
    assert(segs[1]._strokes[1] == strokes[4])
    assert(segs[1]._strokes[2] == strokes[5])
    assert(segs[1].direction == 'down')
    assert(segs[1].status == 'growing')

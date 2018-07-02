from twine_theory.domain import twine_theory as twine

def test_bi_spliting_1():
    ks = [
            ('2018/1/2',11,13,13,11,100)
            ,('2018/1/3',12,14,14,12,100)
            ,('2018/1/4',13,15,15,13,100)
            , ('2018/1/5', 12, 14, 14, 12, 100)
            , ('2018/1/6', 11, 13, 13,11, 100)
            , ('2018/1/7', 9, 11, 11, 9, 100)
            , ('2018/1/8', 7, 9, 9, 7, 100)
            , ('2018/1/8', 5, 7, 7, 5, 100)
        ]

    s = twine.KSeq('day',ks)
    assert len(s._bi) == 1
    assert s._bi[0] == {'from':(0,11),
                        'to':(2,15),
                        'isUp':True,
                        'growing':True
                        }

def test_bi_spliting_2():
    ks = [
            ('2018/1/2',11,13,13,11,100)
            ,('2018/1/3',12,14,14,12,100)
            ,('2018/1/4',13,15,15,13,100)
            , ('2018/1/5', 12, 14, 14, 12, 100)
            , ('2018/1/6', 11, 13, 13,11, 100)
            , ('2018/1/7', 9, 11, 11, 9, 100)
        ]

    s = twine.KSeq('day',ks)
    assert len(s._bi) == 1
    assert s._bi[0] == {'from':(0,11),
                        'to':(2,15),
                        'isUp':True,
                        'growing':True
                        }

def test_bi_spliting_3():
    ks = [
        ('2018-01-02', 13.35, 13.93, 13.7, 13.32, 2081592.5),
        ('2018-01-03', 13.73, 13.86, 13.33, 13.2, 2962498.25),
        ('2018-01-04', 13.32, 13.37, 13.25, 13.13, 1854509.5),
        ('2018-01-05', 13.21, 13.35, 13.3, 13.15, 1210312.75),
        ('2018-01-08', 13.25, 13.29, 12.96, 12.86, 2158620.75),#
        ('2018-01-09', 12.96, 13.2, 13.08, 12.92, 1344345.12),
        ('2018-01-10', 13.04, 13.49, 13.47, 12.92, 2403277.5),
        ('2018-01-11', 13.41, 13.59, 13.4, 13.27, 1443877.75),
        ('2018-01-12', 13.45, 13.68, 13.55, 13.41, 1353991.38),
        ('2018-01-15', 13.51, 14.33, 14.2, 13.5, 3122394.5),
        ('2018-01-16', 14.17, 14.38, 14.2, 14.02, 2444549.0),
        ('2018-01-17', 14.33, 14.8, 14.23, 14.2, 2656294.0),
        ('2018 - 01 - 18', 14.4, 14.72, 14.72, 14.28, 2148027.0),
        ('2018 - 01 - 19', 14.8, 15.13, 14.8, 14.68, 2571146.75),#
        ('2018 - 01 - 22', 14.6, 14.94, 14.44, 14.43, 2073867.25),
        ('2018 - 01 - 23', 14.36, 14.9, 14.65, 14.33, 2388791.75),
        ('2018 - 01 - 24', 14.66, 15.08, 14.64, 14.5, 2591292.25),
        ('2018 - 01 - 25', 14.45, 14.47, 14.2, 14.0, 2369984.75),
        ('2018 - 01 - 26', 14.18, 14.34, 14.05, 14.02, 2032988.62),
        ('2018 - 01 - 29', 14.05, 14.25, 13.74, 13.6, 2090546.75),
        ('2018 - 01 - 30', 13.7, 13.84, 13.65, 13.55, 1094739.88)
        ]

    s = twine.KSeq('day',ks)

    assert len(s._bi) == 2
    assert s._bi[0] == {'from':(0,13.93),
                        'to':(4,12.86),
                        'isUp':False,
                        'growing':False
                        }
    assert s._bi[1] == {'from':(4,12.86),
                        'to':(13,15.13),
                        'isUp':True,
                        'growing':True
                        }

def test_bi_spliting_4():
    ks = [
        ("2017-01-03",9.11,9.18,9.16,9.09,459840.47),
        ("2017-01-04",9.15,9.18,9.16,9.14,449329.53),
        ("2017-01-05",9.17,9.18,9.17,9.15,344372.91),
        ("2017-01-06",9.17,9.17,9.13,9.11,358154.19),
        ("2017-01-09",9.13,9.17,9.15,9.11,361081.56),
        ("2017-01-10",9.15,9.16,9.15,9.14,241053.95),
        ("2017-01-11",9.14,9.17,9.14,9.13,303430.88),
        ("2017-01-12",9.13,9.17,9.15,9.13,428006.75),
        ("2017-01-13",9.14,9.19,9.16,9.12,434301.38),
        ("2017-01-16",9.15,9.16,9.14,9.07,683165.81),
        ("2017-01-17",9.12,9.16,9.15,9.1,545552.38),
        ("2017-01-18",9.14,9.19,9.17,9.13,574269.38),
        ("2017-01-19",9.15,9.24,9.18,9.15,437712.88),
        ("2017-01-20",9.17,9.23,9.22,9.17,393328.56),
        ("2017-01-23",9.22,9.26,9.22,9.2,420299.31),
        ("2017-01-24",9.23,9.28,9.27,9.2,470244.09),
        ("2017-01-25",9.27,9.28,9.26,9.25,304401.97),
        ("2017-01-26",9.27,9.34,9.33,9.26,420712.56)
         ]
         
    s = twine.KSeq('day',ks)
    assert len(s._bi) == 1

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

#standard situation a2

##             9 
##             /\
##            /  \   
##        6  /    \  
##        /\/      \ 
##       / 5        \     4
##      /            \    /\
##     /              \  /  \
##    3                \/    \
##                     2      \
##                            1    
def test_seg_split_a2():
    s = twine.KSeq('day',[])
    s._bi = [
        {'from':(0,3),'to':(1,6),'isUp':True,'growing':False},
        {'from':(1,6),'to':(2,5),'isUp':False,'growing':False},
        {'from':(2,5),'to':(3,9),'isUp':True,'growing':False},
        {'from':(3,9),'to':(4,2),'isUp':False,'growing':False},
        {'from':(4,2),'to':(5,4),'isUp':True,'growing':False},
        {'from':(5,4),'to':(6,1),'isUp':False,'growing':False}
        ]
    s.makeupSegment()
    
    assert(2 == len(s._segment))
    assert(s._segment[0] == {
        'from': (0,3),
        'to': (3,9),
        'isUp': True,
        'bi': [0,1,2],
        'growing':False
        })
    assert(s._segment[1] == {
        'from': (3,9),
        'to': (6,1),
        'isUp': False,
        'bi': [3,4,5],
        'growing':True
        })

#standard situation e
##                               12
##                               /\   11
##                              /  \  /\   10
##                  9          /    \/  \  /\
##         8        /\        /     9    \/  \
##         /\      /  \ 7    /           8    \
##        /  \    /    \/\  /                 7
##       /    \  /     6  \/    
##      /      \/         5
##     /       4         
##    3                
##                     
##                     
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
        'growing':True
        })
    assert(s._segment[2] == {
        'from': (6,5),
        'to': (10,11),
        'isUp': True,
        'bi': [6,7,8],
        'growing':True
        })
    assert(s._segment[3] == {
        'from': (10,11),
        'to': (13,7),
        'isUp': False,
        'bi': [9,10,11],
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


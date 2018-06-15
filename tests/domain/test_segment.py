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
    assert len(s._bi) == 2
    assert s._bi[0] == {'from':(0,11),
                        'to':(2,15),
                        'isUp':True,
                        'growing':False
                        }
    assert s._bi[1]['to']

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
                        'growing':False
                        }


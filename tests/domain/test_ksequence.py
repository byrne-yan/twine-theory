from twine_theory.domain import twine_theory as twine

def test_kseq_ktype():
    assert 'up'==twine.kseq_type(twine.K('2018-5-24',10,12,12,10,1),\
                                  twine.K('2018-5-25',11,13,13,11,1),\
                                  twine.K('2018-5-26',12,14,14,12,1))

    assert 'down'==twine.kseq_type(twine.K('2018-5-24',14,14,12,12,1),\
                                  twine.K('2018-5-25',13,13,11,11,1),\
                                  twine.K('2018-5-26',12,12,10,10,1))

    assert 'top'==twine.kseq_type(twine.K('2018-5-24',10,12,12,10,1),\
                                  twine.K('2018-5-25',13,14,14,13,1),\
                                  twine.K('2018-5-26',10,12,12,10,1))

    assert 'bottom'==twine.kseq_type(twine.K('2018-5-24',11,13,13,11,1),\
                                  twine.K('2018-5-25',10,12,12,10,1),\
                                  twine.K('2018-5-26',11,13,13,11,1))

    assert 'unnormalized'==twine.kseq_type(twine.K('2018-5-24',10,20,20,10,1),\
                                  twine.K('2018-5-25',12,18,18,12,1),\
                                  twine.K('2018-5-26',14,16,16,14,1))

    assert 'unnormalized'==twine.kseq_type(twine.K('2018-5-24',14,16,16,14,1),\
                                  twine.K('2018-5-25',12,18,18,12,1),\
                                  twine.K('2018-5-26',10,20,20,10,1))
def test_kseq_listofdict():
    listDict = [
                    {'time':'2018/1/2','start':13.35,'high':13.93,'end':13.7,'low':13.32,'volume':2081592.5}
                    ,{'time':'2018/1/3','start':13.73,'high':13.86,'end':13.33,'low':13.2,'volume':2962498.25}
                    ,{'time':'2018/1/4','start':13.32,'high':13.37,'end':13.25,'low':13.13,'volume':1854509.5}#
                    ,{'time':'2018/1/5','start':13.21,'high':13.35,'end':13.3,'low':13.15,'volume':1210312.75}#
                    ,{'time':'2018/1/8','start':13.25,'high':13.29,'end':12.96,'low':12.86,'volume':2158620.75}
                    ,{'time':'2018/1/9','start':12.96,'high':13.2,'end':13.08,'low':12.92,'volume':1344345.12}
                    ,{'time':'2018/1/10','start':13.04,'high':13.49,'end':13.47,'low':12.92,'volume':2403277.5}
                    ,{'time':'2018/1/11','start':13.41,'high':13.59,'end':13.4,'low':13.27,'volume':1443877.75}
                    ,{'time':'2018/1/12','start':13.45,'high':13.68,'end':13.55,'low':13.41,'volume':1353991.38}
                    ,{'time':'2018/1/15','start':13.51,'high':14.33,'end':14.2,'low':13.5,'volume':3122394.5}
                    ,{'time':'2018/1/16','start':14.17,'high':14.38,'end':14.2,'low':14.02,'volume':2444549}
                    ,{'time':'2018/1/17','start':14.33,'high':14.8,'end':14.23,'low':14.2,'volume':2656294}
                ]
    s = twine.KSeq('day',listDict)
    assert len(s._seq)==12
    assert s._seq[0].start==13.35
    assert s._seq[0].end == 13.7
    assert s._seq[0].high == 13.93
    assert s._seq[0].low == 13.32
    assert not s._seq[0].merged
    assert not s._seq[1].merged
    assert s._seq[2].merged
    assert s._seq[3].merged
    assert s._seq[4].merged
    assert s._seq[5].merged
    assert not s._seq[6].merged
    
def test_kseq_listoftuple():
    ks = [
            ('2018/1/2',13.35,13.93,13.7,13.32,2081592.5)
            ,('2018/1/3',13.73,13.86,13.33,13.2,2962498.25)
            ,('2018/1/4',13.32,13.37,13.25,13.13,1854509.5)
        ]

    s = twine.KSeq('day',ks)
    assert len(s._seq)==3
    assert s._seq[0].start==13.35
    assert s._seq[0].end == 13.7
    assert s._seq[0].high == 13.93
    assert s._seq[0].low == 13.32

    
def test_kseq_merge():
    ks = [
     ('2018/3/21',11.95,12.12,11.9,11.85,1445109.5)
    ,('2018/3/22',11.9,11.97,11.66,11.62,984278.38)
    ,('2018/3/23',11.25,11.35,11.34,10.92,1825690.75)
    ,('2018/3/26',11.15,11.2,10.93,10.86,1383598.5)#1
    ,('2018/3/27',11.1,11.17,10.94,10.86,1103933.62)#1
    ,('2018/3/28',10.85,11.14,10.89,10.79,1099023.38)#2
    ,('2018/3/29',10.92,11.17,11.05,10.55,1330602.38)#2
    ,('2018/3/30',11.04,11.05,10.9,10.88,752173.69)#2
    ,('2018/4/2',10.87,10.99,10.71,10.7,1109316.38)#2
    ,('2018/4/3',10.6,10.67,10.56,10.51,890745.69)
    ,('2018/4/4',10.68,11.01,10.87,10.6,1602488.75)
    ,('2018/4/9',10.8,11.1,11.02,10.73,1074795.75)
    ,('2018/4/10',11.02,11.46,11.42,10.97,1390950.75)
        ]

    s = twine.KSeq('day',ks)
##    import pdb;pdb.set_trace()
    assert s._norm[3].merged
    assert s._norm[3].ingredient == [3,4]
    assert s._norm[4].merged
    assert s._norm[4].ingredient == [5,6,7,8]
    assert s._seq[3].merged == s._norm[3]
    assert s._seq[4].merged == s._norm[3]
    assert s._seq[5].merged == s._norm[4]
    assert s._seq[6].merged == s._norm[4]
    assert s._seq[7].merged == s._norm[4]
    assert s._seq[8].merged == s._norm[4]

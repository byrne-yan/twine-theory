import sys
print(sys.path)

from twine_theory.domain import twine_theory as tt

def test_k_init():
    k = tt.K("2018/5/21",11.07	,11.11,	10.95,	10.93,	763533.62)
    assert k.time == "2018/5/21"
    assert k.start ==11.07
    assert k.high==11.11
    assert k.end == 10.95
    assert k.low==10.93
    assert k.volume==763533.62
    assert k.level == 1

def test_trend_init():
    tt.Trend(tt.K(2018-05-02,10.97,11.03,10.88,10.8,1190523.25),\
             tt.K(2018-05-03,10.86,10.88,10.75,10.57,1281355.62),\
             tt.K(2018-05-04,10.73,10.83,10.68,10.66,710509.5),\
             tt.K(2018-05-07,10.7,10.83,10.81,10.64,974309.69),\
             tt.K(2018-05-08,10.83,11.15,11.01,10.8,1373305.62),\
             tt.K(2018-05-09,10.98,11.03,10.97,10.88,627656.12)
             )
    
#def test_twine_init():
    
#    zs = Twine(Trend(),\
#               Trend(),\
#               Trend(),\
#               )
#    assert zs.zg = 
#    assert zs.zd =
#    assert zs.gg =
#    assert zs.dd =

from twine_theory.domain import twine_theory as twine
from twine_theory.domain import normalizer as norm

def test_normalizer_ktype():
    assert 'up'==norm.kseq_type(twine.K('2018-5-24',10,12,12,10,1),\
                                  twine.K('2018-5-25',11,13,13,11,1),\
                                  twine.K('2018-5-26',12,14,14,12,1))

    assert 'down'==norm.kseq_type(twine.K('2018-5-24',14,14,12,12,1),\
                                  twine.K('2018-5-25',13,13,11,11,1),\
                                  twine.K('2018-5-26',12,12,10,10,1))

    assert 'top'==norm.kseq_type(twine.K('2018-5-24',10,12,12,10,1),\
                                  twine.K('2018-5-25',13,14,14,13,1),\
                                  twine.K('2018-5-26',10,12,12,10,1))

    assert 'bottom'==norm.kseq_type(twine.K('2018-5-24',11,13,13,11,1),\
                                  twine.K('2018-5-25',10,12,12,10,1),\
                                  twine.K('2018-5-26',11,13,13,11,1))

    assert 'unnormalized'==norm.kseq_type(twine.K('2018-5-24',10,20,20,10,1),\
                                  twine.K('2018-5-25',12,18,18,12,1),\
                                  twine.K('2018-5-26',14,16,16,14,1))

    assert 'unnormalized'==norm.kseq_type(twine.K('2018-5-24',14,16,16,14,1),\
                                  twine.K('2018-5-25',12,18,18,12,1),\
                                  twine.K('2018-5-26',10,20,20,10,1))

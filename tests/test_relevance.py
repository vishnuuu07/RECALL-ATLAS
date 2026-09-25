from pipeline.relevance import classify
def test_direct_attempt_is_not_generic():
    label,depth,_=classify('I tried several searches but cannot find the photo');assert label=='DIRECT' and depth=='E2'
def test_generic_storage_is_not_direct():
    assert classify('The subscription storage billing is wrong')[0] != 'DIRECT'

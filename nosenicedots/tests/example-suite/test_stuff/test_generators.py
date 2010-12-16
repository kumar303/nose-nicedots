
def _passing_test(x):
    pass

def test_gen():
    for x in range(4):
        yield _passing_test, (x,)

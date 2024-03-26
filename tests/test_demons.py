import time


def test_pass():
    time.sleep(2.5)

def test_print():
    print("1234")
    print("不妥协优化")
def test_failed():
    assert 1 == 2

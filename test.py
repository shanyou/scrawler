import re
import os


def test_gen():
    yield "abc"


if __name__ == '__main__':
    res = test_gen()
    print type(res)
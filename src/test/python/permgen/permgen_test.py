import random
import unittest
import perm


class MyNestedFor(perm.NestedFor):
    trace = None

    def setUp(self):
        self.trace = []

    def do_element(self, indexes):
        self.trace.append(indexes[:])


class TestNestedFor(unittest.TestCase):
    def test_get_dim_sizes(self):
        mnf = MyNestedFor()
        ds = mnf.get_dim_sizes([['x', 'y', 'z'], ['u', 'v'], ['a', 'b', 'c', 'd']])
        self.assertEqual([3, 2, 4], ds)

    def test_loop_onedim(self):
        mnf = MyNestedFor()
        mnf.loop([1])
        self.assertEqual(mnf.trace, [[0]])
        mnf = MyNestedFor()
        mnf.loop([3])
        self.assertEqual([[0], [1], [2]], mnf.trace)

    def test_loop_twodim(self):
        mnf = MyNestedFor()
        mnf.loop([1, 1])
        self.assertEqual([[0, 0]], mnf.trace)
        mnf = MyNestedFor()
        mnf.loop([2, 3])
        self.assertEqual([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]], mnf.trace)


if __name__ == '__main__':
    unittest.main()

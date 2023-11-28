import os
import threading
import unittest

from genutility.test import parametrize

from atomicarray import ArrayInt32
from atomicarray.int import PairUint64


class IntTest(unittest.TestCase):
    @parametrize(
        (PairUint64,),
        (ArrayInt32,),
    )
    def test_init(self, cls):
        a = cls(111, 222)
        self.assertEqual(a[0], 111)
        self.assertEqual(a[1], 222)
        with self.assertRaises(IndexError):
            a[2]

    @parametrize(
        (PairUint64,),
        (ArrayInt32,),
    )
    def test_iadd(self, cls):
        a = cls(1, 2)
        b = cls(3, 4)
        a += b
        self.assertEqual(a[0], 4)
        self.assertEqual(a[1], 6)
        self.assertEqual(list(a), [4, 6])

    @parametrize(
        (PairUint64,),
        (ArrayInt32,),
    )
    def test_iadd_thread(self, cls):
        num_workers = os.cpu_count() or 8
        N = 100000

        a = cls(0, 0)
        b = cls(1, 2)

        def target():
            # nonlocal a
            for i in range(N):
                a.__iadd__(b)

        threads = [threading.Thread(target=target) for i in range(num_workers)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        truth = [N * num_workers, 2 * N * num_workers]
        self.assertEqual(list(a), truth)

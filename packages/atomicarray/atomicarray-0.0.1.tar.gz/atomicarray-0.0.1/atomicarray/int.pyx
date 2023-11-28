from libc.stdint cimport int32_t, uint64_t
from libcpp.limits cimport numeric_limits
from libcpp.vector cimport vector

from .atomic cimport DoubleAtomicInt64


cdef class PairUint64:
	""" Pair of 64bit uints. They can be added atomically using `cmpxchg16b` instruction,
		even when the GIL is not held."""

	cdef DoubleAtomicInt64[uint64_t] ai

	def __init__(PairUint64 self, uint64_t a, uint64_t b):
		self.ai = DoubleAtomicInt64[uint64_t](a, b)

	def __iadd__(PairUint64 self, PairUint64 other):
		self.ai.iadd(other.ai)
		return self

	def __getitem__(PairUint64 self, int i):
		if i >= 0 and i < len(self):
			return self.ai.get(i)
		else:
			raise IndexError(i)

	def __len__(PairUint64 self):
		return 2

	def to_tuple(PairUint64 self):
		# this one is not atomic
		return tuple(<uint64_t[:2]> (self.ai.val))

cdef class ArrayInt32:
	""" Array of 32 bit ints. Can be added and read atomically with the help of the GIL. """

	cdef vector[int32_t] arr

	def __init__(ArrayInt32 self, *args):
		self.arr.reserve(len(args))
		for item in args:
			if numeric_limits[int32_t].min() <= item <= numeric_limits[int32_t].max():
				self.arr.push_back(item)
			else:
				raise ValueError("int32_t range exceeded")

	def __iadd__(ArrayInt32 self, ArrayInt32 other):
		if len(self) != len(other):
			raise ValueError("Can only add arrays of same length")

		for i in range(len(self)):
			self.arr[i] += other.arr[i]
		return self

	def __isub__(ArrayInt32 self, ArrayInt32 other):
		if len(self) != len(other):
			raise ValueError("Can only add arrays of same length")

		for i in range(len(self)):
			self.arr[i] -= other.arr[i]
		return self

	def __getitem__(ArrayInt32 self, size_t i):
		return self.arr.at(i)

	def __len__(ArrayInt32 self):
		return len(self.arr)

	def to_tuple(ArrayInt32 self):
		return tuple(self.arr)

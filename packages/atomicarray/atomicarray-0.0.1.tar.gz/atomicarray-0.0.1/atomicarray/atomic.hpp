#include <cstdint>
#include <iostream>
#include <tuple>

#ifdef _MSC_VER
#include <intrin.h>
#endif

template <typename T> class DoubleAtomicInt64 {
public:
  T val[2];

  DoubleAtomicInt64() {}

  DoubleAtomicInt64(T a, T b) {
    val[0] = a;
    val[1] = b;
  }

  void operator=(const DoubleAtomicInt64 &other) {
    val[0] = other.val[0];
    val[1] = other.val[1];
  }

  DoubleAtomicInt64 operator-() { return DoubleAtomicInt64(-val[0], -val[1]); }

  void iadd(const DoubleAtomicInt64 &other) {
    // https://stackoverflow.com/questions/18177622/how-to-atomically-add-and-fetch-a-128-bit-number-in-c
    // https://stackoverflow.com/questions/4825400/cmpxchg16b-correct

#ifdef _MSC_VER
    T olddst[2];

    olddst[0] = val[0];
    olddst[1] = val[1];

    do {
    } while (!_InterlockedCompareExchange128(
        (__int64 *)val, other.val[1] + olddst[1], other.val[0] + olddst[0],
        (__int64 *)olddst));

#else
    val[0] += other.val[0];
    val[1] += other.val[1];
#endif
  }

  T get(size_t i) const { return val[i]; }
};

int main(void) {
  DoubleAtomicInt64<uint64_t> a(1, 2);
  DoubleAtomicInt64<uint64_t> b(3, 4);
  a.iadd(b);
  std::cout << a.get(0) << a.get(1);
}

from z3 import *
from math import ceil, log2

def popcount(bvec):
    return Sum([ZeroExt(int(ceil(log2(bvec.size()))), Extract(i,i,bvec)) for i in range(bvec.size())])

v = [BitVec(f'v{i}', 32) for i in range(20)]

data = [0x81002, 0x1000, 0x29065, 0x29061, 0x0, 0x0, 0x16C40, 0x16C00, 0x20905, 0x805, 0x10220, 0x220, 0x98868, 0x80860, 0x21102, 0x21000, 0x491, 0x481, 0x31140, 0x1000, 0x801, 0x0, 0x60405, 0x400, 0x0C860, 0x60, 0x508, 0x400, 0x40900, 0x800, 0x12213, 0x10003, 0x428C0, 0x840, 0x840C, 0x0C, 0x43500, 0x2000, 0x8105A, 0x1000]

s = Solver()

for i in range(20):
    s.add(v[i] & 0xFFF00000 == 0)
    s.add(data[i * 2] & v[i] == data[i * 2 + 1])

for i in range(20):
    for j in range(18):
        s.add(And(((v[i] >> j) & 7) != 7, ((v[i] >> j) & 7) != 0))

for k in range(20):
    v12 = BitVecVal(0, 32)
    for i in range(20):
        v12 = (v12 | (((v[i] >> k) & 1) << i))
    for j in range(18):
        s.add(And(((v12 >> j) & 7) != 7, ((v12 >> j) & 7) != 0))

for i in range(20):
    s.add(popcount(v[i]) == 10)

for k in range(20):
    v19 = BitVecVal(0, 32)
    for i in range(20):
        v19 = (v19 | (((v[i] >> k) & 1) << i))
    s.add(popcount(v19) == 10)

if s.check() == sat:
    m = s.model()
    for i in range(20):
        print(m[v[i]])
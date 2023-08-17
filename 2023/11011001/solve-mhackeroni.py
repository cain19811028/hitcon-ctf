#!/usr/bin/env python3
# @dp_1, @mebeim - 2020-11-29
# https://mhackeroni.it/archive/2020/12/05/hitcon2020-all-writeups.html#11011001

import z3

table = [0x81002, 0x1000, 0x29065, 0x29061, 0x2, 0x2, 0x16C40, 0x16C00,
		 0x20905, 0x805, 0x10220, 0x220, 0x98868, 0x80860, 0x21102,
		 0x21000, 0x491, 0x481, 0x31140, 0x1000, 0x801, 0x0, 0x60405,
		 0x400, 0x0C860, 0x60, 0x508, 0x400, 0x40900, 0x800, 0x12213,
		 0x10003, 0x428C0, 0x840, 0x840C, 0x0C, 0x43500, 0x2000, 0x8105A,
		 0x1000]

def popcount(v):
	'''
	Bit Twiddling Hacks FTW
	https://graphics.stanford.edu/~seander/bithacks.html#CountBitsSetParallel
	'''
	w = v - ((v >> 1) & 0x55555555)
	q = (w & 0x33333333) + ((w >> 2) & 0x33333333)
	s = ((q + (q >> 4) & 0xF0F0F0F) * 0x1010101) >> 24
	return s

solver = z3.Solver()
inp = [z3.BitVec('x{:02d}'.format(i), 8 * 4) for i in range(20)]

for i, x in enumerate(inp):
	solver.add(x & 0xFFF00000 == 0)
	solver.add(x & table[2 * i] == table[2 * i + 1])

	mask = 7
	for j in range(18):
		solver.add((x & mask) != (7<<j), x & mask != 0)
		mask = mask << 1

for off in range(20):
	for i in range(1, len(inp)-1):
		x = ((inp[i-1]>>off) & 1) + ((inp[i]>>off) & 1) + ((inp[i+1]>>off) & 1)
		solver.add(x != 0, x != 3)

for v in inp:
	solver.add(popcount(v) == 10)

for off in range(20):
	x = (inp[0] >> off) & 1
	for i in range(1, len(inp)):
		x += (inp[i] >> off) & 1
	solver.add(x == 10)

res = solver.check()
assert res == z3.sat

m = solver.model()
nums = [m[x].as_long() for x in inp]
print(*nums)
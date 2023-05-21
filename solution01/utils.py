import collections
import copy
import functools
import itertools
import math
import operator
import re
import sys
import typing
from collections import Counter, defaultdict, deque
from copy import deepcopy
from functools import reduce
from pprint import pprint

readline = lambda x: open("../day_04/input.txt").read().strip().split("\n")


def lmap(func, *iterables):
    return list(map(func, *iterables))


# 1D list for a 2d list
flatten = lambda x: [q for w in x for q in w ]

def add_tuples(a, b):
    return tuple(sum(tup) for tup in zip(a, b))
sign = lambda x : 1 if x > 0 else (-1 if x < 0 else x)
# get the digits in a number
digits = lambda x: [int(q) for q in str(x)]

minmax = lambda x: (min(x), max(x))


def ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"-?\d+", s))  # thanks mserrano!


def positive_ints(s: str) -> typing.List[int]:
    return lmap(int, re.findall(r"\d+", s))  # thanks mserrano!


def floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"-?\d+(?:\.\d+)?", s))


def positive_floats(s: str) -> typing.List[float]:
    return lmap(float, re.findall(r"\d+(?:\.\d+)?", s))


def words(s: str) -> typing.List[str]:
    return re.findall(r"[a-zA-Z]+", s)


def binary_search(f, lo=0, hi=None):
    """
    Returns a value x such that f(x) is true.
    Based on the values of f at lo and hi.
    Assert that f(lo) != f(hi).
    """
    lo_bool = f(lo)
    if hi is None:
        offset = 1
        while f(lo + offset) == lo_bool:
            offset *= 2
        hi = lo + offset
    else:
        assert f(hi) != lo_bool
    best_so_far = lo if lo_bool else hi
    while lo <= hi:
        mid = (hi + lo) // 2
        result = f(mid)
        if result:
            best_so_far = mid
        if result == lo_bool:
            lo = mid + 1
        else:
            hi = mid - 1
    return best_so_far


BLANK = object()


def hamming_distance(a, b) -> int:
    return sum(i is BLANK or j is BLANK or i != j for i, j in itertools.zip_longest(a, b, fillvalue=BLANK))


def edit_distance(a, b) -> int:
    n = len(a)
    m = len(b)
    dp = [[None] * (m + 1) for _ in range(n + 1)]
    dp[n][m] = 0

    def aux(i, j):
        assert 0 <= i <= n and 0 <= j <= m
        if dp[i][j] is not None:
            return dp[i][j]
        if i == n:
            dp[i][j] = 1 + aux(i, j + 1)
        elif j == m:
            dp[i][j] = 1 + aux(i + 1, j)
        else:
            dp[i][j] = min((a[i] != b[j]) + aux(i + 1, j + 1), 1 + aux(i + 1, j), 1 + aux(i, j + 1))
        return dp[i][j]

    return aux(0, 0)


class UnionFind:
    # n: int
    # parents: List[Optional[int]]
    # ranks: List[int]
    # num_sets: int

    def __init__(self, n: int) -> None:
        self.n = n
        self.parents = [None] * n
        self.ranks = [1] * n
        self.num_sets = n

    def find(self, i: int) -> int:
        p = self.parents[i]
        if p is None:
            return i
        p = self.find(p)
        self.parents[i] = p
        return p

    def in_same_set(self, i: int, j: int) -> bool:
        return self.find(i) == self.find(j)

    def merge(self, i: int, j: int) -> None:
        i = self.find(i)
        j = self.find(j)

        if i == j:
            return

        i_rank = self.ranks[i]
        j_rank = self.ranks[j]

        if i_rank < j_rank:
            self.parents[i] = j
        elif i_rank > j_rank:
            self.parents[j] = i
        else:
            self.parents[j] = i
            self.ranks[i] += 1
        self.num_sets -= 1


dirs_2d_4 = [(0, 1), (1, 0), (0, -1), (-1, 0), (0,0)]
dmap = {
    'U' : (0, 1),
    'R' : (1, 0),
    'D' : (0, -1),
    'L' : (-1, 0)
}
neighbors_2d = [(x, y) for y in range(-1, 2) for x in range(-1, 2)  if (x, y) != (0, 0)]

def find_neighbors_2d_8(x,y):
    return [(x + dx, y + dy) for dy in range(-1, 2) for dx in range(-1, 2) if (dx, dy) != (0, 0)]

neighbors_3d = [(x, y, z) for z in range(-1, 2) for y in range(-1, 2) for x in range(-1, 2) if sum((x != 0, y != 0, z!= 0)) == 1]

neighbors_3d = [(-1,0,0), (0,-1,0), (0,0,-1), (1,0,0), (0,1,0), (0,0,1)]



def _neighbors_3d(p):
    return [add_tuples(p, n) for n in neighbors_3d]

neighbors_4d = [(x, y, z, w) for w in range(-1, 2) for z in range(-1, 2) for y in range(-1, 2) for x in range(-1, 2) if
                (x, y, z, w) != (0, 0, 0, 0)]

# 3dirs

# 4dirs
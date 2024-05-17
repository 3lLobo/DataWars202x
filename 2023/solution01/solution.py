# cp from https://github.com/kermitnirmit/Advent-of-Code-2022/blob/master/day_24/solution.py

from utils import *

f = [x for x in open("../input").read().strip().split("\n")]

class Blizzard:
    def __init__(self, loc, dir):
        self.loc = loc
        self.dir = dir
    def __repr__(self):
        return str(self.loc) + "| " + str(self.dir)


start = (0, f[0].index("."))
end = (len(f) - 1, f[-1].index("."))
oldb = set()
dmap = {
    ">": (0,1),
    "^": (-1,0),
    "<": (0,-1),
    "v": (1,0),
}
oldb = set()
bpoints = set()
for i, line in enumerate(f):
    for j, letter in enumerate(line):
        if letter in "<>v^":
            bpoints.add((i, j))
            b = Blizzard((i, j), dmap[letter])
            oldb.add(b)

maxTime = 600 # lcm and pypy don't play nicely so i'm just hardcoding this
times = [bpoints]
for t in range(maxTime):
    newBlizzards = set()
    newBlizzardPoints = set()
    for blizzard in oldb:
        b = blizzard.loc
        dir = blizzard.dir
        si, sj = b
        di, dj = dir

        ni = si + di
        nj = sj + dj

        if 0 >= ni:
            ni = len(f) - 2
        elif len(f) - 1 <= ni:
            ni = 1
        if 0 >= nj:
            nj = len(f[0]) - 2
        elif len(f[0]) - 1 == nj:
            nj = 1

        b = Blizzard((ni, nj), dir)
        newBlizzards.add(b)
        newBlizzardPoints.add((ni, nj))
    times.append(newBlizzardPoints)
    oldb = newBlizzards

def distToEnd(goal, a):
    return abs(goal[0] - a[0]) + abs(goal[1]-a[1])

@functools.lru_cache(maxsize=None)
def solve(startPos, goalPos, startTime):
    q = deque([(startPos, startTime)])
    visited = set()
    while q:
        state = q.popleft()
        curr, steps = state


        if (curr, steps) in visited:
            continue
        if curr == goalPos:
            return steps
        else:
            visited.add((curr, steps))
            i, j = curr
            for di, dj in dirs_2d_4:
                ni, nj = i + di,  j + dj
                if (ni, nj) == goalPos:
                    return steps + 1
                if (1 <= ni < len(f) - 1 and 1 <= nj < len(f[0]) - 1) or (ni, nj) == curr:
                    npoint = (ni, nj)
                    if npoint not in times[(steps + 1) % maxTime]:
                        q.append((npoint, steps + 1))
start_to_finish = solve(start, end, 0)
print(start_to_finish)
last_time = solve(start, end, solve(end, start, start_to_finish))
print(last_time)

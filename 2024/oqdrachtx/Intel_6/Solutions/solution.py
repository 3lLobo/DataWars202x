# Solution: 1023.
# Done and correct.

# Easiest way is to google "tower of hanoi 10 disks minimum moves"

# Otherwise:
# Alternatively, the problem is simply a conversion of the number of bits: 
print(int('1'*10, base=2))

# Alternative alternative: 
def TowerOfHanoi(pieces: int, total_moves: int):
    total_moves += 1
    if pieces==1:
        #print ("Move disk 1 from source",source,"to destination",destination)
        return total_moves
    total_moves = TowerOfHanoi(pieces-1, total_moves)
    total_moves = TowerOfHanoi(pieces-1, total_moves)    
    return total_moves

n = 10
print(TowerOfHanoi(pieces=n, total_moves=0)) 


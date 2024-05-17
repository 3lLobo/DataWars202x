"""
For this solution we create a class for every type in the list and overload the __gt__ function of the classes to compare to each other;
"""

base = "2024/oqdrachtx/Verdediging_3/Saber Force Blaster (pt. 1)/"

with open(base + "input.txt", "r") as f:
    lines = f.readlines()

player1, player2 = lines


class F:
    def __gt__(self, other):
        if isinstance(other, L):
            return True
        return False


class B:
    def __gt__(self, other):
        if isinstance(other, F):
            return True
        return False


class L:
    def __gt__(self, other):
        if isinstance(other, B):
            return True
        return False


player1_moves = eval(player1.split(":")[1].strip(" \n"))
player2_moves = eval(player2.split(":")[1].strip(" \n"))

wins = 0
ties = 0
losses = 0

for player1_move, player2_move in zip(player1_moves, player2_moves):
    if player1_move == player2_move:
        ties += 1
    elif player1_move() > player2_move():
        wins += 1
    else:
        losses += 1

print(f"losses: {losses}, ties: {ties}, wins: {wins}")
print(f"answer should be: {losses}{ties}{wins}")

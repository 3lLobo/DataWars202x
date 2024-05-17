"""
For this solution we create a class for every type in the list and overload the __gt__ function of the classes to compare to each other;

The introduced F count logic keeps track if the 'I always win condition' is applicable in the current state.
"""

base = "2024/oqdrachtx/Verdediging_4/Saber Force Blaster (pt. 2)/"

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

player1_F_count = 0
player2_F_count = 0

for player1_move, player2_move in zip(player1_moves, player2_moves):
    if isinstance(player1_move(), F):
        player1_F_count += 1
        player1_F_count = min(player1_F_count, 3)
    else:
        player1_F_count = 0

    if isinstance(player2_move(), F):
        player2_F_count += 1
        player2_F_count = min(player2_F_count, 3)
    else:
        player2_F_count = 0

    if player1_F_count == 3:
        if player2_F_count == 3:
            ties += 1
        else:
            wins += 1
    elif player2_F_count == 3:
        losses += 1
    elif player1_move == player2_move:
        ties += 1
    elif player1_move() > player2_move():
        wins += 1
    else:
        losses += 1

print(f"losses: {losses}, ties: {ties}, wins: {wins}")
print(f"answer should be: {losses}{ties}{wins}")

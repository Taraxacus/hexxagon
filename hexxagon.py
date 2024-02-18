#!/usr/bin/python
# Author: Maximilian Weinberg
# Date: 2024-02-18
# hexxagon.py: An imitation of the game at hexxagon.com

DIRS = (( 1, 0), ( 1, 1), ( 0, 1), (-1, 0), (-1,-1), ( 0,-1))
FIELD = [[0 for y in range(9)] for x in range(9)]

SYMBOLS = "_OX  "

def add(dir1, dir2):
    return (dir1[0] + dir2[0], dir1[1] + dir2[1])

def reachable(pos,jumps=True):
    r1 = [add(pos, direction) for direction in DIRS]
    if not jumps:
        return r1
    r2 = [add(pos2, direction) for direction in DIRS for pos2 in r1]
    print("Valid moves for {0} are {1}. Direct moves are {2}".format(pos, r2, r1))
    return r2

for x in range(9):
    for y in range(9):
        if abs(x-y)>4:
            FIELD[x][y] = 3
        elif (x,y) in [(3,3),(4,5),(5,4)]:
            FIELD[x][y] = 3
        elif (x,y) in [(4,0), (0,4), (8,8)]:
            FIELD[x][y] = 1
        elif (x,y) in [(0,0), (8,4), (4,8)]:
            FIELD[x][y] = 2

def field_to_string(field, wide=False):
    r = ""
    for a in range(17):
        for b in range(9):
            if (a+b)%2 == 1:
                r += SYMBOLS[4]
            else:
                x = b
                y = 6 - (a-b)//2
                if 0<=x<=8 and 0<=y<=8:
                    r += SYMBOLS[field[x][y]]
                else:
                    r += SYMBOLS[3]
            if wide:
                r += SYMBOLS[4] *3
        r += "\n"
    return r

def is_valid_move(field, player, pos1, pos2):
    if not field[pos1[0]][pos1[1]] == player:
        print("Player is not at position! Instead {0}.".format(field[pos1[0]][pos1[1]]))
        return False
    elif FIELD[pos2[0]][pos2[1]] == 3:
        print("Destination position is off board!")
        return False
    elif pos2 in reachable(pos1, True):
        return True
    else:
        print("Destination position is unreachable!")
        return False

def move(field, player, pos1, pos2):
    # Presupposes move validity
    if pos2 in reachable(pos1, False):
        field[pos2[0]][pos2[1]] = player
        for direction in DIRS:
            pos3 = add(pos2, direction)
            if 0<=pos3[0]<=8 and 0<=pos3[1]<=8:
                if field[pos3[0]][pos3[1]] == 3-player:
                    field[pos3[0]][pos3[1]] = player
        print("Walking move {0} to {1} executed.".format(pos1, pos2))
    elif pos2 in reachable(pos1, True):
        field[pos2[0]][pos2[1]] = player
        field[pos1[0]][pos1[1]] = 0
        for direction in DIRS:
            pos3 = add(pos2, direction)
            if 0<=pos3[0]<=8 and 0<=pos3[1]<=8:
                if field[pos3[0]][pos3[1]] == 3-player:
                    field[pos3[0]][pos3[1]] = player
        print("Jumping move {0} to {1} executed.".format(pos1, pos2))
    else:
        print("Something went wrong...")

def get_move(player, field):
    while True:
        print(field_to_string(field, True))
        input_list = input("PLAYER {0}> ".format(player)).split()
        if len(input_list) == 4:
            try:
                coor_list = [int(coor) for coor in input_list]
                if all(0<=coor<=8 for coor in coor_list):
                    c = coor_list
                    return [(c[0], c[1]), (c[2], c[3])]
                else:
                    print("Invalid input!")
            except:
                print("Invalid input!")
        print("Invalid input!")

def count(field, value):
    return sum(field[x][y] == value for x in range(9) for y in range(9))

def play():
    field = FIELD.copy()
    running = True
    while True:
        while True:
            pos1, pos2 = get_move(1, field)
            if is_valid_move(field, 1, pos1, pos2):
                break
            print("Is invalid move!")
            print(pos1, pos2)
        print("Executing move {0}, {1} for player 1...".format(pos1, pos2))
        move(field, 1, pos1, pos2)
        if any(count(field, value)==0 for value in [0,1,2]):
            break
        while True:
            pos1, pos2 = get_move(2, field)
            if is_valid_move(field, 2, pos1, pos2):
                break
            print("Is invalid move!")
        print("Executing move {0}, {1} for player 2...".format(pos1, pos2))
        move(field, 2, pos1, pos2)
        if any(count(field, value)==0 for value in [0,1,2]):
            break
    print(field_to_string(field))
    difference = count(field,1) - count(field,2)
    if difference > 0:
        print("Player 1 has won!")
    elif difference < 0:
        print("Player 2 has won!")
    else:
        print("It's a tie!")

def main():
    #print(field_to_string(FIELD, True))
    play()

if __name__=="__main__":
    main()

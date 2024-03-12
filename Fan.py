from time import sleep
from Extras_ import UI
import os

rgb = ["color 1", "color 2", "color 6", "color 4"]
blade = "X"
blank = " "
size = 15
fan = [[blank for i in range(size)] for j in range(size)]
for i in range(size):
    for j in range(size):
        if i==int((size-1)/2) or j==int((size-1)/2):
            fan[i][j] = blade

def Center():
    return int((size-1)/2)

def ShowFan(i):
    os.system(rgb[i%len(rgb)])
    UI.Clear()
    print("RTX 4090\n\n")
    print("/-----------------------------------------------------------------------------------------\\")
    for line in fan:
        print("|" + " ".join(line) + "|" + " ".join(line) + "|" + " ".join(line) + "|")
    print("\-----------------------------------------------------------------------------------------/")

def MoveLeft(x, y):
    try:
        fan[y][x-1] = blade
        fan[y][x] = blank
    except:
        pass

def MoveRight(x, y):
    try:
        fan[y][x+1] = blade
        fan[y][x] = blank
    except:
        pass

def Reset_X():
    global total_right, total_left
    total_right = 0
    total_left = 0

def Reset_Y():
    global total_down, total_up
    total_down = 0
    total_up = 0

def Sum_X():
    global total_right, total_left
    total_right += 1
    total_left += 1

def Sum_Y():
    global total_down, total_up
    total_down += 1
    total_up += 1

def Sub_X():
    global total_right, total_left
    total_right -= 1
    total_left -= 1

def Sub_Y():
    global total_down, total_up
    total_down -= 1
    total_up -= 1

def MoveDown(x, y):
    try:
        fan[y+1][x] = blade
        fan[y][x] = blank
    except:
        pass

def MoveUp(x, y):
    try:
        fan[y-1][x] = blade
        fan[y][x] = blank
    except:
        pass

def Start():
    #Primeira movimentação
    i = 0
    while i<60:
        Reset_X()
        Reset_Y()
        while fan[0][0] != blade:
            ShowFan(i)
            move_down = True
            for y in range(size):
                move_right = True
                down_moves = 0
                for x in range(size):
                    if fan[y][x] == blade:
                        #Mover Pra esquerda
                        if y<Center()-total_left and x<=Center():
                            MoveLeft(x,y)
                        #Mover pra direita
                        if y>Center()+total_right and x>=Center() and move_right:
                            MoveRight(x,y)
                            move_right = False
                        #Mover pra baixo
                        if y>=Center() and x<Center()-total_down and move_down:
                            MoveDown(x,y)
                            down_moves += 1
                        #Mover pra cima
                        if y<=Center() and x>Center()+total_up:
                            MoveUp(x,y)
                    if down_moves >= Center()-total_down:
                        move_down = False
            Sum_Y()
            Sum_X()
            sleep(0.001)
        i+=1
        #Segunda movimentação
        Sub_X()
        Sub_Y()
        while fan[Center()][0] != blade:
            ShowFan(i)
            move_down = True
            for y in range(size):
                move_right = True
                down_moves = 0
                for x in range(size):
                    if fan[y][x] == blade:
                        #1 quadrante pra cima
                        if y>Center() and x>Center():
                            MoveUp(x,y)
                        #2 quadrante pra esquerda
                        if y<Center() and x>Center():
                            MoveLeft(x,y)
                        #3 quadrante pra baixo
                        if y<Center() and x<Center()-total_down and move_down:
                            MoveDown(x,y)
                            down_moves += 1
                        #4 quadrante pra direita
                        if y>Center() and x<Center()-total_right and move_right:
                            MoveRight(x,y)
                            move_right = False
                    if down_moves >= Center()-total_down:
                        move_down = False
            Sub_X()
            Sub_Y()
            sleep(0.001)
        i+=1
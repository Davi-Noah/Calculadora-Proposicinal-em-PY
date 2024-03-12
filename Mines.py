from random import randrange as rand
from math import sin, cos, radians as rad
from Extras_ import UI

#Mostrar tabela do jogo com coordenadas nons eixos
def ShowTable(matriz):
    UI.SetTitle("Campo Minado")
    print("   " + " ".join([alf[i] for i in range(len(matriz[0]))]))
    print("   " + " ".join(["-" for i in range(len(matriz[0]))]))
    for i in range(len(matriz)):
        print(f"{alf[i]}| " + "|".join(map(str, matriz[i])) + f" |{alf[i]}")
    print("   " + " ".join(["-" for i in range(len(matriz[0]))]))
    print("   " + " ".join([alf[i] for i in range(len(matriz[0]))]))

#Criar tabela x por y
def Create(x, y):
    return [[0 for i in range(x)] for j in range(y)]

def Cos(angle):
    return round(cos(rad(angle)))

def Sin(angle):
    return round(sin(rad(angle)))

def AddAdjacent(x, y):
    for i in range(0, 360, 45):
        X, Y = x+Cos(i), y+Sin(i)
        try:
            if X>=0 and Y>=0:
                table[X][Y] += 1
        except:
            pass

#Adicionar 1 aos adjacentes de bombas
def PrepareNumbers():
    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j] == bomb:
                AddAdjacent(i, j)

#Gerar bombas baseado no local da primeira jogada
def GenerateBombs(bombs, f_x, f_y):
    while bombs > 0:
        x, y = rand(len(table)), rand(len(table[0]))
        if table[x][y] != bomb and (abs(x-f_x) > 2 or abs(y-f_y) > 2):
            table[x][y] = bomb
            bombs -= 1
    PrepareNumbers()

def Reveal(x, y):
    mask[x][y] = table[x][y]

def GetInput(first):
    while True:
        ShowTable(mask)
        coord = input("\nCoordenadas: ").replace(" ", "")
        coord = coord.upper()
        if len(coord) == 2 and coord[0] in y_alf and coord[1] in x_alf:
            return alf.index(coord[0]), alf.index(coord[1])
        if len(coord) == 3 and coord[0].upper() == "F" and coord[1] in y_alf and coord[2] in x_alf and not first:
            return coord[0].upper(), [alf.index(coord[1]), alf.index(coord[2])]

def Cleanse(x,y):
    Reveal(x,y)
    for i in range(0, 360, 45):
        X, Y = x+Cos(i), y+Sin(i)
        try:
            if table[X][Y] != bomb and X>=0 and Y>=0:
                Reveal(X,Y)
                if table[X][Y] == 0:
                    table[X][Y] = "0"
                    Cleanse(X,Y)
        except:
            pass

def ChooseSettings():
    global table, x_alf, y_alf, bombs
    table = Create(x=20, y=20)
    x_alf = [alf[i] for i in range(len(table[0]))]
    y_alf = [alf[i] for i in range(len(table))]
    bombs = 80

######################################################################################################

bomb = "B"
alf = "ABCDEFGHIJKLMNOPQRSTUVXWYZ"

def Play():
    ChooseSettings()

    global mask
    mask = [["X" for i in range(len(table[0]))] for j in range(len(table))]
    playing = True

    #Geração de bombas após primeiro comando
    ShowTable(mask)
    x, y = GetInput(True)
    GenerateBombs(bombs, x, y)
    Reveal(x,y)
    Cleanse(x,y)

    while playing:
        x, y = GetInput(False)
        if x == "F":
            x, y = map(int,y)
            if mask[x][y] == "X":
                mask[x][y] = "F"
        elif table[x][y] == 0:
            Cleanse(x,y)
        elif table[x][y] != bomb:
            Reveal(x,y)
        else:
            Reveal(x,y)
            ShowTable(table)
            input("\nPerdeukkkjjkk")
            playing = False
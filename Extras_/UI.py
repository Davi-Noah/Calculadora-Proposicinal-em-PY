import os

def Clear():
    os.system("cls")

def SetTitle(string: str):
    Clear()
    print(string+"\n")

def ShowBank(bank: list):
    for i in range(len(bank)):
        show =  " ".join(map(str, bank[i]))
        print(f"{i+1} --> {show}")
    print()

def GetBankEquation(bank: list, ambient: str):
    if len(bank) == 0:
        input("Banco vazio, pressione enter para continuar...")
        return "Empty"
    selecting = True
    while selecting:
        ShowBank(bank)
        try:
            select = input("Selecione uma equação:")
            if 0 < int(select) <= len(bank):
                selecting = False
            else:
                input("\nEquação não existe")
        except:
            if select.upper() == "E":
                return "Exit"
        if selecting:
            SetTitle(ambient)
    return int(select)-1

def GetValidInput(title: str, string: str, entry: list):
    SetTitle(title)
    while True:
        _input = input(string)
        if _input in entry or _input.upper() in entry:
            return _input
        SetTitle(title)

def ChangeColor(string: str):
    colors = {"AZUL":"color 1", "VERDE":"color 2", "AMARELO":"color 6", "VERMELHO":"color 4", "BRANCO":"color 7"}
    if string in colors:
        os.system(colors[string])

def ShowEq(equation: list):
    sub_equation = [i for i in equation]
    sub_equation = " ".join(map(str, sub_equation))
    sub_equation = sub_equation.replace("True", "V")
    sub_equation = sub_equation.replace("False", "F")
    return sub_equation

def GetEquationsArray(bank: list, ambient: str):
    equations_array, display, selected, finish_flag = [], "", "", ""
    while True:
        Index = GetBankEquation(bank, f"{ambient} {display} {finish_flag}")
        if type(Index) == int:
            if bank[Index] not in equations_array:
                equations_array.append(bank[Index])
                selected += str(Index+1)+" "
                display = "\n\nSelecionados: " + ",".join(selected.split(" ")[:-1])
                if len(equations_array) == 2:
                    finish_flag = "\n\n(E) para finalizar seleção"
            SetTitle(f"{ambient} {display} {finish_flag}")
        elif Index == "Exit" and len(equations_array) >= 2:
            return equations_array
        elif Index == "Empty":
            return "Empty"


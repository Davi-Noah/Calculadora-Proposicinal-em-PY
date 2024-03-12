from Extras_ import UI

Global_Alf = ["P","Q","R","S","T"]
Global_Symbols = [["~","^","v","->","<>"],["não","e","ou","então","se, e somente se"]]
Sym_Flag = False

#Função pra realizar operação
def Operate(symbol: str, a: bool, b: bool):
    #Navegar pelos símbolos e escolher a operação
    if symbol == Global_Symbols[int(Sym_Flag)][1]: 
        return a and b
    elif symbol == Global_Symbols[int(Sym_Flag)][2]:
        return a or b
    elif symbol == Global_Symbols[int(Sym_Flag)][3]:
        if a and not b:
            return False
        else:
            return True
    elif symbol == Global_Symbols[int(Sym_Flag)][4]:
        if a == b:
            return True
        else:
            return False

#Função para ler equação
def Read(equation: list):
    sub_equation = [i for i in equation]
    this_title = f"Resolver equação\n\n" + UI.ShowEq(sub_equation)
    for Letter in Global_Alf:
        if Letter in sub_equation:
            value = UI.GetValidInput(this_title, f"Valor de {Letter} (V ou F):", ["V","F"])
            value = value.upper() == "V"
            while Letter in sub_equation:
                next_change = sub_equation.index(Letter)
                sub_equation[next_change] = value
                this_title = f"Resolver equação\n\n" + UI.ShowEq(sub_equation)
    UI.SetTitle(this_title)
    input("Equação pronta, enter para resolver")
    UI.SetTitle("Resolver equação")
    return sub_equation

#Função pra resolver uma equação válida
def Execute(array: list, steps: bool, mask: list):
    title = "Resolver equação"
    #Procurar parênteses para encontrar as prioridades
    while "(" in array:
        mask = [i for i in array]
        if steps:
            UI.SetTitle(title)
            print(UI.ShowEq(array))
        building = False
        #Construir o interior dos elementos dentro dos parênteses
        for i in range(len(array)):
            if array[i] == "(":
                PriorArray = []
                building = True
                Delete_Flag = i
            elif array[i] == ")":
                break
            elif building:
                PriorArray.append(array[i])
        #Remover elementos restantes dos parênteses e criar máscara para interface
        #mask = [[antes], [meio], [depois]]
        Total_Deletes = len(PriorArray)+1
        mask = [array[:Delete_Flag+1], array[Delete_Flag+Total_Deletes:]]
        array[Delete_Flag] = Execute(PriorArray, steps, mask)
        del array[Delete_Flag+1:Delete_Flag+1+Total_Deletes]
        mask = []
        
    #Passar pelos valores da lista até encontrar uma operação (enquanto seu tamanho for maior que 1)
    while len(array) > 1:
        #Navegar pelos símbolos em ordem de precedência
        for symbol in Global_Symbols[int(Sym_Flag)]:
            #Manter aquele símbolo até efetuar todos
            while symbol in array:
                if steps:
                    UI.SetTitle(title)
                    if len(mask):
                        print(UI.ShowEq(mask[0]),UI.ShowEq(array),UI.ShowEq(mask[1]))
                    else:
                        print(UI.ShowEq(array))
                    input()
                #Encontrar próxima operação com sinal de inversão de valor
                operation_index = array.index(symbol)
                if symbol == Global_Symbols[int(Sym_Flag)][0]:
                    a = array.pop(operation_index+1)
                    array[operation_index] = not a
                else:
                    a, b = array.pop(operation_index-1), array.pop(operation_index)
                    array[operation_index-1] = Operate(symbol, a, b)
    if steps:
        UI.SetTitle(title)
        print(UI.ShowEq(array) + "\n")
    return array[0]

#Função para adicionar símbolos possíveis
def Add_Symbol(possible: list, equation: list, closes: int, ready: bool):
    comands = [i for i in possible]
    limit = len(possible)
    for i in range(len(comands)):
        if comands[i] == "Variáveis:":
            sufix = "(" + ",".join(Global_Alf) + ")"
            limit = len(possible)-1
        else:
            sufix = f" ({i+1})"
        comands[i] += sufix
    comands = "\n".join(map(str, comands))
    while True:
        UI.SetTitle("Adicionar equação")
        if len(equation):
            print(f"{' '.join(equation)}\n")
        if closes == 0 and ready:
            print("Digite (Pronto) para salvar equação no banco")
        select = input(f"{comands}\nInput:")

        #Verificar possibilidade da saída
        if closes == 0 and ready and select.upper() == "PRONTO":
            return "Exit"

        #Verificar o tipo da entrada
        try:
            select = int(select)
            if 1 <= select <= limit:
                return select
        except:
            if select.upper() in Global_Alf and limit == len(possible)-1:
                return select.upper()
            
#Função pra criar equação
def Create():
    new_equation: list = []
    #Valores iniciais possíveis = "~", "VAR", "("
    _not = Global_Symbols[int(Sym_Flag)][0]
    avaiable = [_not,"(","Variáveis:"]
    closes_needed, can_finish = 0, False

    while True:
        #Iniciar a pedida de símbolos possíveis
        next_command = Add_Symbol(avaiable, new_equation, closes_needed, can_finish)
        if next_command == "Exit":
            UI.SetTitle("Adicionar equação\n\n" + " ".join(new_equation))
            break
        elif type(next_command) == str:
            new_equation.append(next_command)
        else:
            new_equation.append(avaiable[next_command-1])
        
        #Filtrar próximas possibilidades e suas consequências
        last = new_equation[-1]
        can_finish = last in Global_Alf or last == ")"
        if last in Global_Alf:
            avaiable = Global_Symbols[int(Sym_Flag)][1:]
        else:
            if last == _not:
                avaiable = ["(", "Variáveis:"]
            elif last in Global_Symbols[int(Sym_Flag)][1:]:
                avaiable = [_not, "(", "Variáveis:"]
            elif last == "(":
                closes_needed += 1
                avaiable = [_not, "(", "Variáveis:"]
            elif last == ")":
                closes_needed -= 1
                avaiable = Global_Symbols[Sym_Flag][1:]
        if closes_needed > 0 and (last in Global_Alf or last == ")"):
            avaiable.insert(0, ")")
    
    return new_equation

#Função pra adicionar equação ao banco
def Add(equation: list, bank: list):
    bank.append(equation)

#Função para criar uma tabela verdade
def GenerateTable(equations: list):
    all_tests = [i for i in equations]
    test_types, total_equations, total_results, order = [],[],[],[]
    #Saber quantas variáveis eu tenho
    for equation in all_tests:
        for letter in Global_Alf:
            if letter in equation and letter not in order:
                order.insert(Global_Alf.index(letter), letter)
    #Executar pra cada equação
    for equation in all_tests:
        #Substituir variáveis por números de referência
        total_equations.append(" ".join(equation))
        equation = [i for i in equation]
        for letter in Global_Alf:
            if letter in equation:
                while letter in equation:
                    equation[equation.index(letter)] = order.index(letter)
        #Gerar variações com N variáveis
        total_variations = GetVariations(len(order))
        #Executar para cada variação
        this_result = []
        for variation in total_variations:
            test_equation = [i for i in equation]
            for i in range(len(test_equation)):
                item = test_equation[i]
                if type(item) == int:
                    test_equation[i] = variation[item]
            this_result.append(Execute(test_equation, False, []))
        total_results.append(this_result)
        if this_result.count(True) == 0:
            test_types.append("Contradição")
        elif this_result.count(False) == 0:
            test_types.append("Tautologia")
        else:
            test_types.append("Contingência")
    #Adicionar resultado ao array de variações
    space, comp = 0, 0
    for result in total_results:
        for i in range(len(result)):
            total_variations[i].append(result[i])
            for j in range(len(total_variations[0])):
                space = 0
                if j >= len(order):
                    equation_size = len(total_equations[j-len(order)])/2
                    comp = 1 if equation_size%1==0 else 0
                    space = int(equation_size)
                match total_variations[i][j]:
                    case True:
                        total_variations[i][j] = " "*space + "V" + " "*(space-comp)
                    case False:
                        total_variations[i][j] = " "*space + "F" + " "*(space-comp)
    #Mostrar na tela os resultados
    result_names = [i for i in order + total_equations]
    total_variations.insert(0, result_names)
    for i in total_variations:
        print(" | ".join(map(str, i)))
    print()
    for i in range(len(all_tests)):
        print(" ".join(all_tests[i]) + f" = {test_types[i]}")

#Gerar variações de possibilidades baseadas em uma quatidade de variáveis
def GetVariations(num: int):
    arr = [[0 for i in range(num)] for j in range(2**num)]
    for i in range(num):
        value = False
        for j in range(2**num):
            if j % (2**num/(2**(i+1))) == 0:
                value = not value
            arr[j][i] = value
    return arr

def SwitchReading(bank: list):
    for equation in bank:
        for i in range(len(equation)):
            old_array = Global_Symbols[int(not Sym_Flag)]
            new_array = Global_Symbols[int(Sym_Flag)]
            if equation[i] in old_array:
                equation[i] = new_array[old_array.index(equation[i])]
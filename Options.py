from Extras_ import UI
from Calculator import Boolean_Calculator as Calculator

Read_Modes, read_switch = ["simbólico", "escrito"], False

def Configure(bank):
    global read_switch
    while True:
        Options = f'''Opções

(1) Modo de leitura: {Read_Modes[int(read_switch)]}

(E) Sair de opções

Comando:'''
        UI.Clear()
        action = input(Options).upper()
        match action:
            case "1":
                read_switch = not read_switch
                Calculator.Sym_Flag = not Calculator.Sym_Flag
                Calculator.SwitchReading(bank)
            case "E":
                break

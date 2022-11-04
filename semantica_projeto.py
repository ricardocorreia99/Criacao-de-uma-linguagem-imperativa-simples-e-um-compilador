import re
import ply.yacc as yacc
import sys
from projeto_analisador_lexico import tokens



## funções auxiliares:


# se a função retornar 1 é porque a variável  já foi declarada, se retornar 0 é porque não foi
def check_variable(variavel,variaveis_dic):
  if variavel in variaveis_dic:
    return 1
  else:
    return 0


# esta função retorna o valor do stackPointer de uma variável VarInt
def return_sp_VarInt(variavel,variaveis_dic):
  sp=variaveis_dic[variavel][0]
  return sp


# esta função retorna o valor do stackPointer de uma variável ArrayInt
def return_sp_ArrayInt(variavel,variaveis_dic):
  sp=variaveis_dic[variavel][1]
  return sp


# esta função retorna a dimensaõ de um ArrayInt 1D
def return_dimensions_ArraInt1D(variavel,variaveis_dic):
  dim=variaveis_dic[variavel][0]
  return [dim]


# esta função retorna uma lista:[dimensão,n_linhas,n_colunas] de um ArrayInt 2D
def return_dimensions_ArraInt2D(variavel,variaveis_dic):
  dim=variaveis_dic[variavel][0][0]
  n_linhas=variaveis_dic[variavel][0][1]
  n_colunas=variaveis_dic[variavel][0][2]
  return [dim,n_linhas,n_colunas]




# retorna o tipo
def return_tipo(variavel,variaveis_dic):
    tipo=variaveis_dic[variavel][2]
    return tipo











def p_programa(p):
    "programa : declaracoes statements"

    p[0] = p[1] + p[2]
    parser.guardar = p[0]
    if(parser.success):
        if (len(parser.aviso1D_variaveis)):
            for key in parser.aviso1D_variaveis:
                print("AVISO! O array " + parser.aviso1D_variaveis[key][0] + " só admite índices entre 0 e "+str(parser.aviso1D_variaveis[key][1])+"!\n")
        if (len(parser.aviso2D_variaveis)):
            for key in parser.aviso2D_variaveis:
                print("AVISO! O array " + parser.aviso2D_variaveis[key][0] + "  admite índices:\nLinhas entre 0 e "+str(parser.aviso2D_variaveis[key][1][1])+"\nColunas entre 0 e "+str(parser.aviso2D_variaveis[key][2][1])+"\n")
        print("Código máquina:\n"+ parser.guardar)
    else:

        print("Código máquina:\n" + parser.guardar)
        print("\n\nExiste erro/os, o código máquina não será gerado para um ficheiro .vm!\nConsulte o erro no código acima.\n")


# -----------------declarações----------------------------------------------------------


def p_declaracoes_vazio(p):
    "declaracoes : "
    p[0] = ""



def p_declaracoes(p):
    "declaracoes : declaracoes declaracao"
    p[0]=p[1]+p[2]


def p_declaracao_declVar(p):
    "declaracao : declVar"
    p[0] = p[1]


def p_declaracao_declArray(p):
    "declaracao : declArray"
    p[0] = p[1]


def p_declVar(p):
    "declVar : VarInt listIds '|'"
    p[0] = p[2]


def p_listIds_ID(p):
    "listIds : ID"
    if (check_variable(p[1], parser.variaveis)):
        p[0] = ("err\"Variável repetida!\"\n") + "stop\n"
        print("A variável \""+p[1]+"\" já foi declarada.\n")
        parser.success = False
    else:
        parser.variaveis[p[1]]=[parser.sp,1,"VarInt"]
        p[0]=("pushi 0\n")
        parser.sp+=1


def p_listIds_ID_listIds(p):
    "listIds : listIds ',' ID"
    if (check_variable(p[3], parser.variaveis)):
        x = ("err\"Variável repetida!\"\n")+ "stop\n"
        print("A variável \"" + p[3] + "\" já foi declarada.\n")
        parser.success = False
    else:
        parser.variaveis[p[3]]=[parser.sp,1,"VarInt"]
        x = ("pushi 0\n")
        parser.sp += 1
    p[0] = p[1] + x


def p_declArray(p):
    "declArray : ArrayInt listIdArray '|'"
    p[0] = p[2]


def p_listIdArray_list_listIdArray(p):
    "listIdArray : listIdArray ',' array"
    p[0] = p[1] + p[3]


def p_listIdArray_list(p):
    "listIdArray : array"
    p[0] = p[1]




def p_list_ID1(p):
    "array : ID '[' Num ']'"
    if (check_variable(p[1], parser.variaveis)):
        p[0] = ("err\"Variável repetida!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" já foi declarada.\n")
        parser.success = False
    else:
        parser.variaveis[p[1]]=[int(p[3]),parser.sp,"ArrayInt"]
        p[0] = (f"pushn {int(p[3])}\n")
        parser.sp += int(p[3])



def p_list_ID2(p):
    "array : ID '[' Num ']' '[' Num ']'"
    if (check_variable(p[1], parser.variaveis)):
        p[0] = ("err\"Variável repetida!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" já foi declarada.\n")
        parser.success = False
    else:
        dim_bi = int(p[3]) * int(p[6]) #dim_bi = numero de elementos
        parser.variaveis[p[1]]=[(dim_bi,int(p[3]),int(p[6])),parser.sp,"DoubleArrayInt"]
        p[0] = (f'pushn {dim_bi}\n')
        parser.sp += dim_bi





# -------------------statements-------------------------------------------------------------------

def p_statements(p):
    "statements : Inicio ':' instrucoes Fim"
    p[0] = "start\n" + p[3] + "stop\n"


def p_instrucoes_instrucao(p):
    "instrucoes : instrucao"
    p[0] = p[1]


def p_instrucoes_instrucao_instrucoes(p):
    "instrucoes : instrucoes instrucao"
    p[0] = p[1] + p[2]


def p_instrucao_atribuicao(p):
    "instrucao : atribuicao"
    p[0] = p[1]


def p_instrucao_se(p):
    "instrucao : se"
    p[0] = p[1]


def p_instrucao_imprimir(p):
    "instrucao : imprimir"
    p[0] = p[1]


def p_instrucao_ciclo(p):
    "instrucao : ciclo"
    p[0] = p[1]


def p_atribuicao_ID_expressao(p):
    "atribuicao : ID '=' expressao '|'"
    # ver se a variavel está declarada. Se nao estiver enviamos um erro

    # Se estiver declarada entao não há erro
    if (check_variable(p[1],parser.variaveis)):
        if (return_tipo(p[1],parser.variaveis)=="VarInt"):
            stackpointer=return_sp_VarInt(p[1],parser.variaveis)
            p[0] = p[3] + f"storeg {stackpointer}\n" 

        else:
            p[0] = ("err\"Indexação em falta!\"\n")+ "stop\n"
            print("A variável \"" + p[1] + "\" precisa de indexação.\n")
            parser.success = False


    else:
        # a variavel nao esta declarada
        p[0] = ("err\"Variável não existe!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" não foi declarada.\n")
        parser.success = False






def p_atribuicao_ID_ler(p):
    "atribuicao : ID '=' Ler '(' ')' '|'"

    # ver se a variavel está declarada. Se nao estiver enviamos um erro
    # Se estiver declarada entao não há erro
    if (check_variable(p[1],parser.variaveis)):
        if(return_tipo(p[1],parser.variaveis)=="VarInt"):
            stackpointer = return_sp_VarInt(p[1], parser.variaveis)
            p[0] = f"read\natoi\n" + f"storeg {stackpointer}\n"
        else:
            p[0] = ("err\"Indexação em falta!\"\n")+ "stop\n"
            print("A variável \"" + p[1] + "\" precisa de indexação.\n")
            parser.success = False
    else:
        # a variavel nao esta declarada
        p[0] = ("err\"Variável não existe!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" não foi declarada.\n")
        parser.success = False





def p_atribuicao_ID_expressao1D(p):
    "atribuicao : ID '[' expressao ']' '=' expressao '|'"
    if (check_variable(p[1],parser.variaveis)):
        if (return_tipo(p[1],parser.variaveis)=="ArrayInt"):
            dim=return_dimensions_ArraInt1D(p[1],parser.variaveis)
            parser.aviso1D_variaveis[p[1]]=[p[1],dim[0]-1]
            stackpointer=return_sp_ArrayInt(p[1],parser.variaveis)
            p[0]= f"pushgp\npushi {stackpointer}\npadd\n" + p[3] + p[6] + "storen\n"
        else:
            p[0] = ("err\"A variável em questão não admite indexação, ou é um array de dimensão diferente!\"\n")+ "stop\n"
            print("A variável \"" + p[1] + "\" não admite indexação, ou é um array de dimensão diferente.\n")
            parser.success = False

    else:
        # a variavel nao esta declarada
        p[0] = ("err\"Variável não declarada!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" não está declarada.\n")
        parser.success = False





def p_atribuicao_ID_ler1D(p):
    "atribuicao : ID '[' expressao ']' '=' Ler '(' ')' '|'"
    if (check_variable(p[1],parser.variaveis)):
        if (return_tipo(p[1], parser.variaveis) == "ArrayInt"):
            dim = return_dimensions_ArraInt1D(p[1], parser.variaveis)
            parser.aviso1D_variaveis[p[1]] = [p[1], dim[0] - 1]
            stackpointer = return_sp_ArrayInt(p[1], parser.variaveis)
            p[0] =f"pushgp\npushi {stackpointer}\npadd\n" + p[3]+ f"read\natoi\n" + f"storen\n"

        else:
            p[0] = ("err\"A variável em questão não admite indexação, ou é um array de dimensão diferente!\"\n")+ "stop\n"
            print("A variável \"" + p[1] + "\" não admite indexação, ou é um array de dimensão diferente.\n")
            parser.success = False

    else:
        # a variavel nao esta declarada
        p[0] = ("err\"Variável não declarada!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" não está declarada.\n")
        parser.success = False





def p_atribuicao_ID_expressao2D(p):
    "atribuicao : ID '[' expressao ']' '[' expressao ']' '=' expressao '|'"
    if (check_variable(p[1],parser.variaveis)):
        if(return_tipo(p[1],parser.variaveis)=="DoubleArrayInt"):
            stackpointer=return_sp_ArrayInt(p[1],parser.variaveis)
            dimensoes=return_dimensions_ArraInt2D(p[1],parser.variaveis)
            colunas=dimensoes[2]
            linhas=dimensoes[1]
            parser.aviso2D_variaveis[p[1]]=[p[1],(0,linhas-1),(0,colunas-1)]
            p[0]= f"pushgp\npushi {stackpointer}\npadd\n" + p[3] + f"pushi {colunas}\n" + "mul\n" + p[6] + "add\n" + p[9] + "storen\n"
        else:
            p[0] = ("err\"A variável em questão não admite indexação, ou é um array de dimensão diferente!\"\n")+ "stop\n"
            print("A variável \"" + p[1] + "\" não admite indexação, ou é um array de dimensão diferente.\n")
            parser.success = False



    else:
        # a variavel nao esta declarada
        p[0] = ("err\"Variável não declarada!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" não está declarada.\n")
        parser.success = False



def p_atribuicao_ID_ler2D(p):
    "atribuicao : ID '[' expressao ']' '[' expressao ']' '=' Ler '(' ')' '|'"
    if (check_variable(p[1],parser.variaveis)):
        if(return_tipo(p[1],parser.variaveis)=="DoubleArrayInt"):
            parser.aviso2D=1
            stackpointer = return_sp_ArrayInt(p[1], parser.variaveis)
            dimensoes = return_dimensions_ArraInt2D(p[1], parser.variaveis)
            colunas = dimensoes[2]
            linhas = dimensoes[1]
            parser.aviso2D_variaveis[p[1]] = [p[1], (0, linhas - 1), (0, colunas - 1)]
            p[0]= f"pushgp\npushi {stackpointer}\npadd\n" + p[3] + f"pushi {colunas}\n" + "mul\n" + p[6]+ "add\n" + f"read\natoi\n" + "storen\n"
        else:
            p[0] = ("err\"A variável em questão não admite indexação, ou é um array de dimensão diferente!\"\n")+ "stop\n"
            print("A variável \"" + p[1] + "\" não admite indexação, ou é um array de dimensão diferente.\n")
            parser.success = False
    else:
        # a variavel nao esta declarada
        p[0] = ("err\"Variável não declarada!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" não está declarada.\n")
        parser.success = False



def p_se_Se(p):
    "se : Se '(' condicoes ')' '{' conteudoSeRep '}'"
    p[0] = p[3] + f"jz fimSe{parser.fimSeCount}\n" + p[6] + f"fimSe{parser.fimSeCount}: nop\n"
    parser.fimSeCount +=1



def p_se_Se_Senao(p):
   "se : Se '(' condicoes ')' '{' conteudoSeRep '}' Senao '{' conteudoSeRep '}'"
   p[0] = p[3] + f"jz senao{parser.senaoCount}\n" + p[6] + f"jump fimSe{parser.fimSeCount}\n" + f"senao{parser.senaoCount}: nop\n" + p[10] + f"fimSe{parser.fimSeCount}: nop\n"
   parser.senaoCount +=1
   parser.fimSeCount +=1



def p_conteudoSeRep_vazio(p):
    "conteudoSeRep : "
    p[0]=""


def p_conteudoSeRep_instrucoes(p):
    "conteudoSeRep : instrucoes"
    p[0]=p[1]


def p_ciclo(p):
   "ciclo : Repete '{' conteudoSeRep '}' Ate '(' condicoes ')'"
   p[0] = f"ciclo{parser.cicloCount}: nop\n" + p[3] + p[7] + f"jz ciclo{parser.cicloCount}\n"
   parser.cicloCount +=1







def p_imprimir_expressao(p):
    "imprimir : Imprimir '(' expressao ')' '|'"
    p[0] = p[3] + "writei\n"
    


def p_imprimir_string(p):
    "imprimir : Imprimir '(' String ')' '|'"
    p[0] = f"pushs {p[3]}\nwrites\n"



def p_elemento_ID(p):
    "elemento : ID"
    if (check_variable(p[1],parser.variaveis)):
        if(return_tipo(p[1],parser.variaveis)=="VarInt"):
            stackpointer=return_sp_VarInt(p[1],parser.variaveis)
            p[0] = f"pushg {stackpointer}\n"
        else:
            p[0] = ("err\"Indexação em falta!\"\n")+ "stop\n"
            print("A variável \"" + p[1] + "\" precisa de indexação.\n")
            parser.success = False


    else:
        p[0] = ("err\"Variável não declarada!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" não está declarada.\n")
        parser.success = False




def p_elemento_ID_expressao1D(p):
    "elemento : ID '[' expressao ']'"
    if (check_variable(p[1],parser.variaveis)):
        if(return_tipo(p[1],parser.variaveis)=="ArrayInt"):
            dim = return_dimensions_ArraInt1D(p[1], parser.variaveis)
            parser.aviso1D_variaveis[p[1]] = [p[1], dim[0] - 1]
            stackpointer = return_sp_ArrayInt(p[1], parser.variaveis)
            p[0] = f"pushgp\npushi {stackpointer}\npadd\n"+p[3]+"loadn\n"

        else:
            p[0] = ("err\"A variável em questão não admite indexação, ou é um array de dimensão diferente!\"\n")+ "stop\n"
            print("A variável \"" + p[1] + "\" não admite indexação, ou é um array de dimensão diferente.\n")
            parser.success = False



    else:
        p[0] = ("err\"Variável não declarada!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" não está declarada.\n")
        parser.success = False





def p_elemento_ID_expressao2D(p):
    "elemento : ID '[' expressao ']' '[' expressao ']'"
    if (check_variable(p[1],parser.variaveis)):
        if (return_tipo(p[1], parser.variaveis) == "DoubleArrayInt"):
            parser.aviso2D=1
            stackpointer = return_sp_ArrayInt(p[1], parser.variaveis)
            dimensoes = return_dimensions_ArraInt2D(p[1], parser.variaveis)
            colunas = dimensoes[2]
            linhas = dimensoes[1]
            parser.aviso2D_variaveis[p[1]] = [p[1], (0, linhas - 1), (0, colunas - 1)]
            p[0] = f"pushgp\npushi {stackpointer}\npadd\n" + p[3] + f"pushi {colunas}\n" + "mul\n" + p[6] + "add\n" + "loadn\n"

        else:
            p[0] = ("err\"A variável em questão não admite indexação, ou é um array de dimensão diferente!\"\n")+ "stop\n"
            print("A variável \"" + p[1] + "\" não admite indexação, ou é um array de dimensão diferente.\n")
            parser.success = False


    else:
        p[0] = ("err\"Variável não declarada!\"\n")+ "stop\n"
        print("A variável \"" + p[1] + "\" não está declarada.\n")
        parser.success = False


def p_expressao_mais(p):
    "expressao : expressao '+' termo"
    p[0] = p[1] + p[3] + "add\n"


def p_expressao_menos(p):
    "expressao : expressao '-' termo"
    p[0] = p[1] + p[3] + "sub\n"


def p_expressao_termo(p):
    "expressao : termo"
    p[0]=p[1]


def p_expressao_and(p):
    "expressao : expressao And termo"
    p[0] = p[1]+p[3]+"mul\n" + "not\n" +"not\n" # retorna 1 ou 0


def p_expressao_or(p):
    "expressao : expressao Or termo"
    p[0] = p[1] + p[3] + "add\n" + p[1] + p[3] + "mul\n" + "sub\n" + "not\n" + "not\n"  # retorna 1 ou 0



def p_expressao_Igualigual(p):
    "expressao : expressao Igualigual termo"
    p[0]=p[1]+p[3]+"equal\n"



def p_expressao_dif(p):
    "expressao : expressao Diferente termo"
    p[0]=p[1]+p[3]+"equal\n"+"not\n"


def p_expressao_Maiorouigual(p):
    "expressao : expressao Maiorouigual termo"
    p[0]=p[1]+p[3]+"supeq\n"



def p_expressao_Menorouigual(p):
    "expressao : expressao Menorouigual termo"
    p[0] = p[1] + p[3] + "infeq\n"


def p_expressao_Not(p):
    "expressao : Not '(' expressao ')'"
    p[0]=p[3]+"not\n"


def p_expressao_Menor_expressao(p):
    "expressao : expressao '<' termo"
    p[0]=p[1]+p[3]+"inf\n"


def p_expressao_Maior_expressao(p):
    "expressao : expressao '>' termo"
    p[0] = p[1] + p[3] + "sup\n"



def p_termo_vezes(p):
    "termo : termo '*' fator"
    p[0] = p[1] + p[3] + "mul\n"


def p_termo_dividir(p):
    "termo : termo '/' fator"
    p[0] = p[1] + p[3] + "div\n"


def p_termo_divisao_inteira(p):
    "termo : termo '%' fator"
    p[0] = p[1] + p[3] + "mod\n"



def p_termo_fator(p):
    "termo : fator"
    p[0]=p[1]


def p_fator_numposneg(p):
    "fator : num_pos_neg"
    p[0]=p[1]


def p_fator_elemento(p):
    "fator : elemento"
    p[0]=p[1]


def p_fator_expressao(p):
    "fator : '(' expressao ')'"
    p[0]=p[2]


def p_numposneg_Num(p):
    "num_pos_neg : Num"
    p[0]= f"pushi {p[1]}\n"


def p_numposneg_Num_neg(p):
    "num_pos_neg : Num_neg"
    p[0] = f"pushi {p[1]}\n"


def p_condicoes_expressao(p):
    "condicoes : expressao"
    p[0]=p[1]


def p_error(p):
    print("Ocorreu um erro sintático: ",p)
    parser.success = False



parser = yacc.yacc()
parser.variaveis = {}
parser.sp = 0
parser.senaoCount= 0
parser.fimSeCount= 0
parser.cicloCount= 0
parser.guardar=""
parser.aviso1D_variaveis={}
parser.aviso2D_variaveis={}



nome1=input("Nome do ficheiro a abrir: ")
file = open(nome1,'r')
contents = file.read()
print(contents)


parser.success = True
res = parser.parse(contents)

if (parser.success):
    nome2=input("Introduz o nome do ficheiro: ")
    ficheiro=open(nome2,'w')
    ficheiro.write(parser.guardar)



import sys

import ply.lex as lex
import re



states=[('comentario','inclusive')]
tokens = ['OFF','IN','VarInt', 'ArrayInt', 'Inicio', 'Fim', 'Se', 'Senao', 'Repete', 'Ate', 'Ler', 'Imprimir', 'String',
         'Num', 'Num_neg','ID', 'Maiorouigual', 'Menorouigual','Igualigual','Diferente','And','Or','Not']


literals = ['*', '+','%' ,'/', '-', '=', '(', ')', '.', '<', '>', ',','{', '}', '[', ']','|',':']





def t_And(t):
    r'\/\\'
    return t

def t_Or(t):
    r'\\\/'
    return t

def t_Not(t):
    r'!'
    return t

def t_Maiorouigual(t):
    r'>='
    return t

def t_Igualigual(t):
    r'=='
    return t

def t_Diferente(t):
    r'=/='
    return t

def t_Menorouigual(t):
    r'<='
    return t

def t_VarInt(t):
    r'VarInt'
    return t

def t_ArrayInt(t):
    r'ArrayInt'
    return t

def t_Inicio(t):
    r'inicio'
    return t

def t_Fim(t):
    r'fim'
    return t

def t_Senao(t):
    r'Senao'
    return t

def t_Se(t):
    r'Se'
    return t


def t_Repete(t):
    r'Repete'
    return t

def t_Ate(t):
    r'Ate'
    return t

def t_Ler(t):
    r'Ler'
    return t

def t_Imprimir(t):
    r'Imprimir'
    return t

def t_comentario(t):
    r'/\*'
    t.lexer.begin('comentario')

def t_comentario_OFF(t):
    r'\*/'
    t.lexer.begin('INITIAL')

def t_comentario_IN(t):
    r'(.|\n)'

def t_String(t):

    r'"[^"]+"'

    return t

def t_Num(t):
    r'\d+'
    return t

def t_Num_neg(t):
    r'\(-\d+\)'
    res = re.search(r'-\d+', t.value)
    t.value = res.group(0)
    return t

def t_ID(t):
    r'\w+'
    return t




t_ignore=' \n\t'

def t_error(t):
    print('Erro léxico, caracter inválido na linha:',t.lexer.lineno)
    t.lexer.skip(1) ## ignora o erro e continua

lexer=lex.lex()












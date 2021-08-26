import sqlite3
from sqlite3 import Error
from tkinter import messagebox
import os

caminho = os.path.dirname(__file__)     # diretório do Banco de Dados
db = caminho + '\\agenda.db'            # path do Banco de Dados => E:\INFORMATICA\PYTHON\PYTHON_PycharmProjects\Agenda\agenda.db

#------------------ Criar Conexão -----------------------------------------
def conectarDB():
    con = None
    try:
        con = sqlite3.connect(db)     # conecta o Banco de Dados
    except Error as erro:
        messagebox.showinfo(title='ERRO', message=erro)
    return con

#------------------------------ Consultas (SELECT) ------------------------------------------
def Consultar(SQL):
    con = conectarDB()
    c = con.cursor()
    c.execute(SQL)
    ver = c.fetchall()           # p/ Consulta de dados
    con.close()
    return ver

#------------------------------ Alterações (INSERT, UPDATE, DELETE) ------------------------------------------
def AtualizarTabela(SQL):
    try:
        con = conectarDB()
        c = con.cursor()
        c.execute(SQL)
        con.commit()
        con.close()
    except Error as erro:
        messagebox.showinfo(title='ERRO', message=erro)








from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import conexao
form = Tk()
form.state('zoomed')               # abre o formulário em tela cheia    # form.geometry('1200x600+50+30')
form.title('Agenda Eber (primeira versão)')
form.wm_iconbitmap('timao.ico')
fundo = '#bb8'
form['bg'] = fundo

#------------------------------------------ Função LimpaEntradas -----------------------------------------------------------
def LimpaEntradas():
    nome.delete(0, END)  # apaga os Entry's
    tel.delete(0, END)
    end.delete(0, END)
    email.delete(0, END)
    nasc.delete(0, END)
    obs.delete(0, END)
    nome.focus()  # aponta para o nome

#------------------------------------------- Função Visualizar() -------------------------------------------------------
def Visualizar():
    tv.delete(*tv.get_children())
    if indice.get() == 'i_cadastro': sql = '''SELECT * FROM Contatos ORDER BY id_contatos'''
    else: sql = '''SELECT * FROM Contatos ORDER BY con_Nome'''
    linhas = conexao.Consultar(sql)
    for i in linhas: tv.insert('','end', values=i)


#------------------------------------------- Função Inserir ------------------------------------------------------------
def Inserir():
    if nome.get() == '':
        messagebox.showinfo(title='Erro', message='Digite pelo menos o nome')
        return
    try:
        sql = 'INSERT INTO Contatos (con_Nome, con_Telefone, con_Endereco, con_Email, con_Nascimento, con_Obs) VALUES ("'+nome.get()+'", "'+tel.get()+'", "' \
                +end.get()+'", "'+email.get() +'", "'+nasc.get()+'", "'+obs.get()+'")'
        print(sql)
        conexao.AtualizarTabela(sql)
    except:
        messagebox.showinfo(title='Erro', message='Erro ao inserir novo registro')
        return
    Visualizar()
    LimpaEntradas()

#------------------------------------------ Função Alterar -----------------------------------------------------------
def Alterar():
    try:
        reg = tv.selection()[0]                     # incluir um Error caso precione o ALTERAR sem escolher antes
        campo = tv.item(reg, 'values')
        global id                               # registro a ser alterado na função Salvar
        id=campo[0]
        nome.insert(0,campo[1])
        tel.insert(0, campo[2])
        end.insert(0, campo[3])
        email.insert(0, campo[4])
        nasc.insert(0, campo[5])
        obs.insert(0, campo[6])
        nome.focus()
        messagebox.showinfo(title='Modificação de Registro', message='Altere os dados e clique em SALVAR')

    except:
        messagebox.showinfo(title='ERRO', message='Nenhum item selecionado para alterar')
        return

#------------------------------------------ Função Salvar -----------------------------------------------------------
def Salvar():
    if nome.get() == '':
        messagebox.showinfo(title='Erro', message='Faltou o nome')
        return
    try:
        sql = 'UPDATE Contatos SET con_Nome= "'+nome.get()+'", con_Telefone="'+tel.get()+'", con_Endereco="'+end.get()+'", con_Email="'\
              +email.get()+'", con_Nascimento="'+nasc.get()+'", con_Obs="'+obs.get()+'" WHERE id_contatos='+id
        print(sql)
        conexao.AtualizarTabela(sql)
    except:
        messagebox.showinfo(title='Erro', message='Erro ao inserir novo registro')
        return
    Visualizar()
    LimpaEntradas()

#----------------------------------------- Função Pesquisar ------------------------------------------------------------
def Pesquisar():
    tv.delete(*tv.get_children())
    if indice.get() == 'i_cadastro': sql = 'SELECT * FROM Contatos WHERE con_Nome LIKE "%'+pesquisarNome.get()+'%" ORDER BY id_contatos'
    else: sql = 'SELECT * FROM Contatos WHERE con_Nome LIKE "%'+pesquisarNome.get()+'%" ORDER BY con_Nome'
    linhas = conexao.Consultar(sql)
    for i in linhas: tv.insert('', 'end', values=i)
    pesquisarNome.delete(0, END)  # apaga os Entry's

#----------------------------------------- Função Deletar --------------------------------------------------------------
def Deletar():      # apaga o registro seleionado
    try:
        reg = tv.selection()[0]
        campo = tv.item(reg, 'values')
        res = messagebox.askyesno(title='Atenção!', message='Confirma a exclusão de '+campo[1]+' ?')
        if (res == True):
            tv.delete(reg)
            sql = 'DELETE FROM Contatos WHERE id_contatos=' + campo[0]
            conexao.AtualizarTabela(sql)
        else:
            Visualizar()
            # return
    except:
        messagebox.showinfo(title='ERRO', message='Nenhum item selecionado para excluir')
        return

#----------------------------------------- Função Cancelar -----------------------------------------------------------------
def Cancelar():
    print('Cancela')
    LimpaEntradas()
    Visualizar()

#----------------------------------------- Função Sair -----------------------------------------------------------------
def Sair():
    form.destroy()


#-------------------------------------- Label Principal ---------------------------------------------------------------
Label(form, text='AGENDA TELEFÔNICA (Cadastro de Amigos)', font=('Time New Roman',15,'italic'), bg=fundo, fg='brown').pack(pady=10)

#--------------------------------------------- Frame Lista de Contatos ------------------------------------------------
fr_Contatos = LabelFrame(form, text='Contatos', bg=fundo, font=('Time New Roman', 10,'bold','italic'))
fr_Contatos.pack(fill='both',padx=10, pady=10, ipady=30)            #  expand='yes',

#--------------------------------------------- TreeView Contato --------------------------------------------
tv = ttk.Treeview(fr_Contatos, columns=('id_contatos','con_Nome','con_Telefone', 'con_Endereco', 'con_Email', 'con_Nascimento', 'con_Obs'),show='headings')
tv.column('id_contatos', minwidth=0, width=30)
tv.column('con_Nome', minwidth=0, width=200)
tv.column('con_Telefone', minwidth=0, width=90)
tv.column('con_Endereco', minwidth=0, width=300)
tv.column('con_Email', minwidth=0, width=200)
tv.column('con_Nascimento', minwidth=0, width=80)
tv.column('con_Obs', minwidth=0, width=420)
tv.heading('id_contatos', text='Reg', anchor=W)
tv.heading('con_Nome', text='Nome', anchor=W)
tv.heading('con_Telefone', text='Telefone', anchor=W)
tv.heading('con_Endereco', text='Endereço', anchor=W)
tv.heading('con_Email', text='Email', anchor=W)
tv.heading('con_Nascimento', text='Nascimento', anchor=W)
tv.heading('con_Obs', text='Observação', anchor=W)
tv.pack()
indice = StringVar()
indice.set('i_cadastro')
Visualizar()

#--------------------------------------------- Frame Inserir Novos Contatos --------------------------------
fr_Inserir = LabelFrame(form, text='Inserir Novos Contatos', bg=fundo, font=('Time New Roman', 10,'bold','italic'), borderwidth=2)
fr_Inserir.pack(fill='both', expand='yes', padx=10, pady=10)

#--------------------------------------------- Label Inserir Novos Contatos --------------------------------
lb_nome=Label(fr_Inserir, text='Nome', bg=fundo)
lb_nome.pack(side='left')
nome=Entry(fr_Inserir, width=20)
nome.pack(side='left', padx=10)

lb_tel=Label(fr_Inserir, text='Tel.', bg=fundo)
lb_tel.pack(side='left')
tel=Entry(fr_Inserir, width=15)
tel.pack(side='left', padx=10)

lb_end=Label(fr_Inserir, text='Endereço', bg=fundo)
lb_end.pack(side='left')
end=Entry(fr_Inserir, width=40)
end.pack(side='left', padx=10)

lb_email=Label(fr_Inserir, text='Email', bg=fundo)
lb_email.pack(side='left')
email=Entry(fr_Inserir, width=25)
email.pack(side='left', padx=10)

lb_nasc=Label(fr_Inserir, text='Nasc.', bg=fundo)
lb_nasc.pack(side='left')
nasc=Entry(fr_Inserir, width=13)
nasc.pack(side='left', padx=10)

lb_obs=Label(fr_Inserir, text='Obs', bg=fundo)
lb_obs.pack(side='left')
obs=Entry(fr_Inserir, width=50)
obs.pack(side='left', padx=10)


#--------------------------------------------- Frame Pesquisar Contatos ----------------------------------------
fr_Pesquisar = LabelFrame(form, text='Pesquisar Contatos', bg=fundo, font=('Time New Roman', 10,'bold','italic'))
fr_Pesquisar.pack(fill='both', expand='Yes', padx=10, pady=10)

#--------------------------------------------- Label Pesquisar Contatos -----------------------------------------
lb_Pnome=Label(fr_Pesquisar, text='Nome', bg=fundo)
lb_Pnome.pack(side='left')
pesquisarNome=Entry(fr_Pesquisar)
pesquisarNome.pack(side='left', padx=10)

#--------------------------------------------- Radio Button  -----------------------------------------------------
indice = StringVar()
indice.set('i_cadastro')          # o default é por ordem de Cadastro

rb_dataCadastro = Radiobutton(fr_Pesquisar, text='Ordem de Cadastro', bg=fundo, width=20, anchor=W, value='i_cadastro', variable=indice)
rb_dataCadastro.place(x=400, y=50)
rb_nome = Radiobutton(fr_Pesquisar, text='Ordem Alfabética', bg=fundo, width=20, anchor=W, value='i_nome', variable=indice)
rb_nome.place(x=550, y=50)
#--------------------------------------------- Botão Deletar ------------------------------------------------------
bt_Deletar = Button(fr_Contatos, text='Deletar', command=Deletar)
bt_Deletar.place(x=1200, y=240)                                                    # bt_Deletar.pack(side='right', padx=40)

#--------------------------------------------- Botão Alterar (puxa os dados para alteração) ----------------------------
bt_Alterar = Button(fr_Contatos, text='Alterar', command=Alterar)
bt_Alterar.place(x=1100, y=240)                      # pack(side='right', padx=10)

#--------------------------------------------- Botão Inserir (inserir novo registro) ----------------------------------
v=80
h=50
w=8
bt_Inserir= Button(fr_Inserir, text='Inserir', command=Inserir, width=w)
bt_Inserir.place(x=h, y=v)

#--------------------------------------------- Botão Salvar (salvar a alteração)
bt_Salvar = Button(fr_Inserir, text='Salvar', command=Salvar, width=w)
bt_Salvar.place(x=h+100, y=v)

#--------------------------------------------- Botão Cancelar (cancelar a alteração)
bt_Salvar = Button(fr_Inserir, text='Cancelar', command=Cancelar, width=w)
bt_Salvar.place(x=h+200, y=v)

#--------------------------------------------- Botão Pesquisar ------------------------------------------------------
bt_Pesquisar = Button(fr_Pesquisar, text='Pesquisar', command=Pesquisar)
bt_Pesquisar.place(x=200, y=50)                               #pack(side='left', padx=10)

#--------------------------------------------- Botão Mostrar ------------------------------------------------------
bt_Mostrar = Button(fr_Pesquisar, text='Mostrar Todos', command=Visualizar)
bt_Mostrar.place(x=300, y=50)                                 #pack(side='left', padx=10)

#--------------------------------------------- Botão Sair --------------------------------------------
bt_Sair = Button(fr_Pesquisar, text='SAIR', command=Sair, font=('Castelar',11,'bold'))
bt_Sair.pack(side='right', padx=50)

form.mainloop()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main.py
# Github:@WeDias

#  MIT License
#
#  Copyright (c) 2020 Wesley Ribeiro Dias
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import tkinter
import sqlite3
from hashlib import sha256
from tkinter import messagebox


def criptografar(string: str) -> str:
    """
    criptografar(): Serve para gerar uma hash sha256 a partir de uma string qualquer
    :param string: str, string usada para gerar a hash
    :return: str, hash sha256
    """
    return sha256(string.encode()).hexdigest()


def dashboard(nome: str) -> None:
    """
    dashboard(): Serve para criar a tela principal do programa apos o login ser realizado com sucesso
    :return: None
    """
    # ------------------------------------------------------------------------------------------------------------------
    # Definicoes da janela_principal/dashboard

    janela_principal = tkinter.Tk()
    janela_principal.geometry('900x520+500+250')
    janela_principal.title('Dashboard')
    janela_principal.iconbitmap('img/ico_spc.ico')
    janela_principal.resizable(False, False)

    # ------------------------------------------------------------------------------------------------------------------
    # Labels janela_principal

    icone_obras = tkinter.PhotoImage(file='img/obras.png')
    tkinter.Label(janela_principal, image=icone_obras).grid(row=0, column=0, padx=150, pady=120)

    tkinter.Label(janela_principal, text=f'Seja bem-vindo {nome} !', font=5, justify='left').place(x=0, y=0)

    # ------------------------------------------------------------------------------------------------------------------
    # Botoes janela_principal

    tkinter.Button(janela_principal, text='Sair').grid(row=1, column=0)

    # ------------------------------------------------------------------------------------------------------------------
    # Fim janela_principal

    janela_principal.focus_force()
    janela_principal.mainloop()


def main() -> None:
    """
    main(): Serve para fazer a tela de login para o usuario
    :return: None
    """

    def entrar() -> None:
        """
        entrar(): Serve para verificar se o usuario e a senha estao corretos e cadastrados no banco de dados
        :return: None
        """
        banco = sqlite3.connect('data/users.db')
        cursor = banco.cursor()
        dados = cursor.execute(f'SELECT * FROM login WHERE usuario = "{ent_entrar.get()}";').fetchone()
        banco.close()
        if dados and criptografar(ent_senha.get()) == dados[1]:
            messagebox.showinfo('Login', 'Login realizado com sucesso clique em OK para continuar')
            janela_login.destroy()
            dashboard(dados[0])
        else:
            messagebox.showerror('Erro', 'Falha ao realizar login, usuário/senha inválido')

    # ------------------------------------------------------------------------------------------------------------------
    # Definicoes da janela_login

    janela_login = tkinter.Tk()
    janela_login.title('Bem-vindo')
    janela_login.iconbitmap('img/ico_spc.ico')
    janela_login.geometry('400x115+700+400')
    janela_login.resizable(False, False)

    # ------------------------------------------------------------------------------------------------------------------
    # Labels janela_login

    tkinter.Label(janela_login).grid(row=0, column=0)

    img = tkinter.PhotoImage(file='img/logo_spc.png')
    lb_img = tkinter.Label(janela_login, image=img)
    lb_img.place(x=230, y=5)

    lb_entrar = tkinter.Label(janela_login, text='Usuário')
    lb_entrar.grid(row=1, column=0)

    lb_senha = tkinter.Label(janela_login, text='Senha')
    lb_senha.grid(row=2, column=0)

    lb_status = tkinter.Label(janela_login)
    lb_status.grid(row=3, column=2, pady=10)

    # ------------------------------------------------------------------------------------------------------------------
    # Botoes janela_login

    btn_entrar = tkinter.Button(janela_login, text='Entrar', width=20, command=entrar, relief='groove', cursor='hand2')
    btn_entrar.grid(row=3, column=1, pady=5)

    # ------------------------------------------------------------------------------------------------------------------
    # Entry janela_login

    ent_entrar = tkinter.Entry(janela_login, width=30)
    ent_entrar.grid(row=1, column=1)

    ent_senha = tkinter.Entry(janela_login, width=30, show='*')
    ent_senha.grid(row=2, column=1)

    # ------------------------------------------------------------------------------------------------------------------
    # Fim janela_login

    janela_login.focus_force()
    janela_login.mainloop()


if __name__ == '__main__':
    main()

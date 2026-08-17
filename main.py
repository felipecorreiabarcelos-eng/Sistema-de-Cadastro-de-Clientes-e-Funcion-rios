"""
Sistema de Cadastro de Clientes e Funcionários
Projeto acadêmico - Python + SQL (SQLite)

Autor: Felipe
Curso: Ciência da Computação (3º período)

Descrição:
    Sistema simples de linha de comando (CLI) para cadastrar,
    listar, buscar, atualizar e remover Clientes e Funcionários,
    utilizando um banco de dados SQLite (biblioteca sqlite3, que já
    vem junto com o Python, não precisa instalar nada).
"""

import sqlite3
import re
from datetime import datetime

NOME_BANCO = "empresa.db"


# ============================================================
# CONEXÃO E CRIAÇÃO DAS TABELAS
# ============================================================

def conectar():
    """Abre uma conexão com o banco de dados SQLite."""
    conexao = sqlite3.connect(NOME_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    """Cria as tabelas de clientes e funcionarios, caso não existam."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            email TEXT,
            telefone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            cargo TEXT,
            salario REAL,
            data_admissao TEXT
        )
    """)

    conexao.commit()
    conexao.close()


# ============================================================
# FUNÇÕES DE VALIDAÇÃO (bem simples, nível iniciante)
# ============================================================

def cpf_valido(cpf):
    """Verifica se o CPF tem 11 dígitos numéricos (validação simples)."""
    cpf = re.sub(r"\D", "", cpf)  # remove tudo que não é número
    return len(cpf) == 11


def email_valido(email):
    """Validação simples: precisa ter '@' e um '.' depois dele."""
    if email == "":
        return True  # email é opcional
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", email) is not None


# ============================================================
# CRUD - CLIENTES
# ============================================================

def cadastrar_cliente(nome, cpf, email, telefone):
    if not nome.strip():
        return False, "O nome não pode ser vazio."
    if not cpf_valido(cpf):
        return False, "CPF inválido. Deve conter 11 dígitos."
    if not email_valido(email):
        return False, "E-mail inválido."

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO clientes (nome, cpf, email, telefone) VALUES (?, ?, ?, ?)",
            (nome, cpf, email, telefone)
        )
        conexao.commit()
        conexao.close()
        return True, "Cliente cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Já existe um cliente com esse CPF."


def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, cpf, email, telefone FROM clientes ORDER BY nome")
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def buscar_cliente_por_nome(nome):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, cpf, email, telefone FROM clientes WHERE nome LIKE ?",
        (f"%{nome}%",)
    )
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def atualizar_cliente(id_cliente, nome, email, telefone):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
        (nome, email, telefone, id_cliente)
    )
    linhas_afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()
    return linhas_afetadas > 0


def deletar_cliente(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    linhas_afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()
    return linhas_afetadas > 0


# ============================================================
# CRUD - FUNCIONÁRIOS
# ============================================================

def cadastrar_funcionario(nome, cpf, cargo, salario, data_admissao=None):
    if not nome.strip():
        return False, "O nome não pode ser vazio."
    if not cpf_valido(cpf):
        return False, "CPF inválido. Deve conter 11 dígitos."
    try:
        salario = float(salario)
        if salario < 0:
            return False, "O salário não pode ser negativo."
    except ValueError:
        return False, "Salário inválido."

    if data_admissao is None:
        data_admissao = datetime.now().strftime("%d/%m/%Y")

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO funcionarios (nome, cpf, cargo, salario, data_admissao) VALUES (?, ?, ?, ?, ?)",
            (nome, cpf, cargo, salario, data_admissao)
        )
        conexao.commit()
        conexao.close()
        return True, "Funcionário cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Já existe um funcionário com esse CPF."


def listar_funcionarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, cpf, cargo, salario, data_admissao FROM funcionarios ORDER BY nome"
    )
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def buscar_funcionario_por_nome(nome):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, cpf, cargo, salario, data_admissao FROM funcionarios WHERE nome LIKE ?",
        (f"%{nome}%",)
    )
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def atualizar_funcionario(id_funcionario, cargo, salario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE funcionarios SET cargo = ?, salario = ? WHERE id = ?",
        (cargo, salario, id_funcionario)
    )
    linhas_afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()
    return linhas_afetadas > 0


def deletar_funcionario(id_funcionario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id_funcionario,))
    linhas_afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()
    return linhas_afetadas > 0


# ============================================================
# MENUS (interface de linha de comando)
# ============================================================

def menu_clientes():
    while True:
        print("\n--- MENU CLIENTES ---")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("3 - Buscar cliente por nome")
        print("4 - Atualizar cliente")
        print("5 - Deletar cliente")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF (somente números): ")
            email = input("E-mail (opcional): ")
            telefone = input("Telefone: ")
            sucesso, mensagem = cadastrar_cliente(nome, cpf, email, telefone)
            print(mensagem)

        elif opcao == "2":
            clientes = listar_clientes()
            if not clientes:
                print("Nenhum cliente cadastrado.")
            for c in clientes:
                print(f"ID {c[0]} | {c[1]} | CPF: {c[2]} | E-mail: {c[3]} | Tel: {c[4]}")

        elif opcao == "3":
            nome = input("Nome (ou parte dele) para buscar: ")
            encontrados = buscar_cliente_por_nome(nome)
            if not encontrados:
                print("Nenhum cliente encontrado.")
            for c in encontrados:
                print(f"ID {c[0]} | {c[1]} | CPF: {c[2]} | E-mail: {c[3]} | Tel: {c[4]}")

        elif opcao == "4":
            id_cliente = input("ID do cliente a atualizar: ")
            nome = input("Novo nome: ")
            email = input("Novo e-mail: ")
            telefone = input("Novo telefone: ")
            if atualizar_cliente(id_cliente, nome, email, telefone):
                print("Cliente atualizado com sucesso!")
            else:
                print("Cliente não encontrado.")

        elif opcao == "5":
            id_cliente = input("ID do cliente a deletar: ")
            if deletar_cliente(id_cliente):
                print("Cliente removido com sucesso!")
            else:
                print("Cliente não encontrado.")

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_funcionarios():
    while True:
        print("\n--- MENU FUNCIONÁRIOS ---")
        print("1 - Cadastrar funcionário")
        print("2 - Listar funcionários")
        print("3 - Buscar funcionário por nome")
        print("4 - Atualizar cargo/salário")
        print("5 - Deletar funcionário")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF (somente números): ")
            cargo = input("Cargo: ")
            salario = input("Salário: ")
            sucesso, mensagem = cadastrar_funcionario(nome, cpf, cargo, salario)
            print(mensagem)

        elif opcao == "2":
            funcionarios = listar_funcionarios()
            if not funcionarios:
                print("Nenhum funcionário cadastrado.")
            for f in funcionarios:
                print(f"ID {f[0]} | {f[1]} | CPF: {f[2]} | Cargo: {f[3]} | Salário: R$ {f[4]:.2f} | Admissão: {f[5]}")

        elif opcao == "3":
            nome = input("Nome (ou parte dele) para buscar: ")
            encontrados = buscar_funcionario_por_nome(nome)
            if not encontrados:
                print("Nenhum funcionário encontrado.")
            for f in encontrados:
                print(f"ID {f[0]} | {f[1]} | CPF: {f[2]} | Cargo: {f[3]} | Salário: R$ {f[4]:.2f} | Admissão: {f[5]}")

        elif opcao == "4":
            id_funcionario = input("ID do funcionário a atualizar: ")
            cargo = input("Novo cargo: ")
            salario = input("Novo salário: ")
            if atualizar_funcionario(id_funcionario, cargo, salario):
                print("Funcionário atualizado com sucesso!")
            else:
                print("Funcionário não encontrado.")

        elif opcao == "5":
            id_funcionario = input("ID do funcionário a deletar: ")
            if deletar_funcionario(id_funcionario):
                print("Funcionário removido com sucesso!")
            else:
                print("Funcionário não encontrado.")

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_principal():
    criar_tabelas()
    while True:
        print("\n===== SISTEMA DE CADASTRO - EMPRESA =====")
        print("1 - Gerenciar Clientes")
        print("2 - Gerenciar Funcionários")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_clientes()
        elif opcao == "2":
            menu_funcionarios()
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()

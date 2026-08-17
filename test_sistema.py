"""
Testes automatizados do Sistema de Cadastro de Clientes e Funcionários.

Usa o módulo unittest (nativo do Python).
Cada teste usa um banco de dados de teste separado (teste.db), para não
misturar com os dados reais do sistema (empresa.db).
"""

import unittest
import os
import main


class TestSistemaCadastro(unittest.TestCase):

    def setUp(self):
        """Executado ANTES de cada teste: cria um banco de dados limpo."""
        main.NOME_BANCO = "teste.db"
        if os.path.exists("teste.db"):
            os.remove("teste.db")
        main.criar_tabelas()

    def tearDown(self):
        """Executado DEPOIS de cada teste: remove o banco de teste."""
        if os.path.exists("teste.db"):
            os.remove("teste.db")

    # ---------------- VALIDAÇÕES ----------------

    def test_cpf_valido(self):
        self.assertTrue(main.cpf_valido("12345678901"))
        self.assertTrue(main.cpf_valido("123.456.789-01"))  # com pontuação
        self.assertFalse(main.cpf_valido("123"))
        self.assertFalse(main.cpf_valido("abc"))

    def test_email_valido(self):
        self.assertTrue(main.email_valido("felipe@teste.com"))
        self.assertTrue(main.email_valido(""))  # vazio é permitido (opcional)
        self.assertFalse(main.email_valido("sememail"))
        self.assertFalse(main.email_valido("sem@arroba"))

    # ---------------- CLIENTES ----------------

    def test_cadastrar_cliente_sucesso(self):
        sucesso, mensagem = main.cadastrar_cliente(
            "Maria Silva", "12345678901", "maria@teste.com", "27999990000"
        )
        self.assertTrue(sucesso)
        clientes = main.listar_clientes()
        self.assertEqual(len(clientes), 1)
        self.assertEqual(clientes[0][1], "Maria Silva")

    def test_cadastrar_cliente_cpf_invalido(self):
        sucesso, mensagem = main.cadastrar_cliente(
            "João", "111", "joao@teste.com", "27988887777"
        )
        self.assertFalse(sucesso)
        self.assertIn("CPF inválido", mensagem)

    def test_cadastrar_cliente_cpf_duplicado(self):
        main.cadastrar_cliente("Ana", "12345678901", "ana@teste.com", "27977776666")
        sucesso, mensagem = main.cadastrar_cliente(
            "Outra Ana", "12345678901", "outra@teste.com", "27966665555"
        )
        self.assertFalse(sucesso)
        self.assertIn("já existe", mensagem.lower())

    def test_buscar_cliente_por_nome(self):
        main.cadastrar_cliente("Carlos Pereira", "11122233344", "", "")
        resultado = main.buscar_cliente_por_nome("Carlos")
        self.assertEqual(len(resultado), 1)
        resultado_vazio = main.buscar_cliente_por_nome("NomeQueNaoExiste")
        self.assertEqual(len(resultado_vazio), 0)

    def test_atualizar_cliente(self):
        main.cadastrar_cliente("Pedro", "22233344455", "pedro@teste.com", "27955554444")
        clientes = main.listar_clientes()
        id_pedro = clientes[0][0]
        atualizado = main.atualizar_cliente(id_pedro, "Pedro Souza", "pedrosouza@teste.com", "27944443333")
        self.assertTrue(atualizado)
        clientes = main.listar_clientes()
        self.assertEqual(clientes[0][1], "Pedro Souza")

    def test_deletar_cliente(self):
        main.cadastrar_cliente("Lucas", "33344455566", "", "")
        clientes = main.listar_clientes()
        id_lucas = clientes[0][0]
        removido = main.deletar_cliente(id_lucas)
        self.assertTrue(removido)
        self.assertEqual(len(main.listar_clientes()), 0)

    # ---------------- FUNCIONÁRIOS ----------------

    def test_cadastrar_funcionario_sucesso(self):
        sucesso, mensagem = main.cadastrar_funcionario(
            "Fernanda Lima", "44455566677", "Analista", "3500.00"
        )
        self.assertTrue(sucesso)
        funcionarios = main.listar_funcionarios()
        self.assertEqual(len(funcionarios), 1)
        self.assertEqual(funcionarios[0][3], "Analista")

    def test_cadastrar_funcionario_salario_invalido(self):
        sucesso, mensagem = main.cadastrar_funcionario(
            "Rafael", "55566677788", "Estagiário", "abc"
        )
        self.assertFalse(sucesso)
        self.assertIn("Salário inválido", mensagem)

    def test_cadastrar_funcionario_salario_negativo(self):
        sucesso, mensagem = main.cadastrar_funcionario(
            "Beatriz", "66677788899", "Gerente", "-100"
        )
        self.assertFalse(sucesso)

    def test_atualizar_funcionario(self):
        main.cadastrar_funcionario("Gustavo", "77788899900", "Assistente", "2000.00")
        funcionarios = main.listar_funcionarios()
        id_gustavo = funcionarios[0][0]
        atualizado = main.atualizar_funcionario(id_gustavo, "Coordenador", 4500.00)
        self.assertTrue(atualizado)
        funcionarios = main.listar_funcionarios()
        self.assertEqual(funcionarios[0][3], "Coordenador")
        self.assertEqual(funcionarios[0][4], 4500.00)

    def test_deletar_funcionario(self):
        main.cadastrar_funcionario("Juliana", "88899900011", "RH", "3000.00")
        funcionarios = main.listar_funcionarios()
        id_juliana = funcionarios[0][0]
        removido = main.deletar_funcionario(id_juliana)
        self.assertTrue(removido)
        self.assertEqual(len(main.listar_funcionarios()), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

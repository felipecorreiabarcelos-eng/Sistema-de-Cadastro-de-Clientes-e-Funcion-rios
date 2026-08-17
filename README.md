# 📋 Sistema de Cadastro de Clientes e Funcionários

Sistema de linha de comando (CLI) em **Python + SQL (SQLite)** para gerenciar
o cadastro de **clientes** e **funcionários** de uma empresa. Projeto
desenvolvido como trabalho acadêmico (Ciência da Computação).

## ✨ Funcionalidades

Para **Clientes** e para **Funcionários**, o sistema oferece um CRUD completo:

- ✅ Cadastrar (com validação de nome, CPF, e-mail e salário)
- 📋 Listar todos os registros
- 🔍 Buscar por nome (busca parcial)
- ✏️ Atualizar dados de um registro
- 🗑️ Remover um registro

## 🛠️ Tecnologias

- **Python 3** — linguagem principal
- **SQLite** (`sqlite3`, nativo do Python) — banco de dados, sem necessidade de instalar servidor
- **unittest** (nativo do Python) — testes automatizados
- **re** (nativo do Python) — validação de CPF e e-mail

Não é necessário instalar nenhuma dependência externa para rodar o sistema
ou os testes — só bibliotecas padrão do Python.

## 📁 Estrutura do projeto

```
sistema-cadastro/
├── main.py              # Sistema principal (banco de dados, CRUD, menus)
├── test_sistema.py       # Testes automatizados (unittest)
├── requirements.txt      # Dependências (só necessário p/ gerar o PDF de doc.)
├── docs/
│   └── Documentacao_Sistema_Cadastro.pdf   # Documentação completa do projeto
├── .gitignore
└── README.md
```

## ▶️ Como executar

Pré-requisito: ter o Python 3 instalado.

```bash
# Clonar o repositório
git clone https://github.com/SEU-USUARIO/sistema-cadastro.git
cd sistema-cadastro

# Rodar o sistema
python main.py
```

O banco de dados (`empresa.db`) é criado automaticamente na primeira execução.

## 🧪 Como rodar os testes

```bash
python -m unittest test_sistema -v
```

O projeto conta com **13 testes automatizados**, cobrindo validações de CPF,
e-mail e salário, além de todas as operações de CRUD de clientes e
funcionários.

## 🗄️ Estrutura do banco de dados

**Tabela `clientes`**

| Coluna    | Tipo                        | Descrição                     |
|-----------|-----------------------------|--------------------------------|
| id        | INTEGER (PK, autoincrement) | Identificador único            |
| nome      | TEXT                        | Nome completo (obrigatório)    |
| cpf       | TEXT (único)                | CPF, sem duplicidade           |
| email     | TEXT                        | E-mail (opcional)              |
| telefone  | TEXT                        | Telefone de contato            |

**Tabela `funcionarios`**

| Coluna         | Tipo                        | Descrição                        |
|----------------|-----------------------------|-----------------------------------|
| id             | INTEGER (PK, autoincrement) | Identificador único               |
| nome           | TEXT                        | Nome completo (obrigatório)       |
| cpf            | TEXT (único)                | CPF, sem duplicidade              |
| cargo          | TEXT                        | Cargo/função                      |
| salario        | REAL                        | Salário (não pode ser negativo)   |
| data_admissao  | TEXT                        | Data de admissão (dd/mm/aaaa)     |

## 📄 Documentação completa

O arquivo [`docs/Documentacao_Sistema_Cadastro.pdf`](docs/Documentacao_Sistema_Cadastro.pdf)
detalha as decisões de projeto, todos os testes realizados (com resultado da
execução) e sugestões de melhorias futuras.

## 🚀 Possíveis melhorias futuras

- [ ] Migrar de SQLite para PostgreSQL/MySQL
- [ ] Criar interface gráfica (Tkinter) ou versão web (Flask/Django)
- [ ] Adicionar autenticação de usuário
- [ ] Gerar relatórios em PDF/Excel direto pelo sistema
- [ ] Validação de CPF com dígitos verificadores reais

## 👤 Autor

Desenvolvido por Felipe — estudante de Ciência da Computação.

## 📝 Licença

Este projeto é de uso livre para fins acadêmicos e de estudo.

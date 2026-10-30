# Sistema de Controle de Acessibilidade e Recursos (acessibilidade)

Este projeto foi desenvolvido como parte da disciplina de Banco de Dados. O objetivo da aplicação é simular a interface entre uma linguagem de programação e o banco de dados MySQL, permitindo gerenciar locais e seus respectivos recursos de acessibilidade de forma eficiente. O sistema adota a arquitetura MVC (Model-View-Controller) e utiliza comandos SQL puros, sem o uso de frameworks ORM.

## Integrantes do Grupo
* Kimberly Alves dos Santos - 25110020

## Informações Acadêmicas
* Professor: Howard Roatti
* Disciplina: Banco de Dados
* Semestre: 2026/2

## Tecnologias Utilizadas
* Banco de Dados: MySQL 8.0 (Engine InnoDB)
* Modelagem: MySQL Workbench
* Linguagem de Programação: Python

---

## Estrutura do Banco de Dados
O banco de dados acessibilidade é composto por duas tabelas principais relacionadas de forma não-identificadora, garantindo a integridade referencial:

* locais: Armazena os estabelecimentos ou locais mapeados (id_local, nome, tipo, endereco, cidade).
* recursos: Armazena os recursos de acessibilidade vinculados a cada local (id_recurso, id_local, nome, tipo_deficiencia, situacao, data_verificacao).

O script de criação inclui uma restrição do tipo CHECK (chk_situacao) para garantir que o estado de um recurso seja estritamente: FUNCIONANDO, EM MANUTENCAO ou INEXISTENTE.

---

## Estrutura do Repositório

O projeto está estruturado de acordo com as especificações do edital da seguinte forma:

```text
├── diagrams/                  # Arquivo editável (.mwb) e imagem (.png) do Modelo Relacional
├── sql/                       # Scripts de criação de tabelas e consultas externas (.sql)
└── src/                       # Código-fonte da aplicação em Python
    ├── conexion/              # Módulo de conexão nativa com o banco de dados MySQL
    ├── controller/            # Controladores de negócio (CRUD e validações estáticas)
    ├── model/                 # Classes e entidades de dados mapeadas
    ├── reports/               # Lógica de renderização de tabelas e consultas externas
    ├── utils/                 # Constantes de configuração, menus de texto e helpers visuais
    └── principal.py           # Arquivo principal de execução do sistema
```

---

## Como Executar o Script de Banco de Dados e Aplicação

### 1. Configurar o Banco de Dados
Acesse o seu ambiente MySQL Workbench ou terminal MySQL e execute o script disponível na pasta sql:

* Executar o arquivo `sql/tabelas_criacao.sql` completo para gerar a estrutura testada.

### 2. Instalação de Dependências da Aplicação
Certifique-se de possuir o interpretador Python instalado no ambiente e instale o conector oficial do MySQL executando o seguinte comando no terminal do seu sistema operacional:

```bash
pip install mysql-connector-python
```

### 3. Configuração de Credenciais
Abra o arquivo `src/conexion/mysql_queries.py` e insira a senha do seu usuário local do MySQL na propriedade correspondente:

```python
self.password = "SUA_SENHA_AQUI"
```

### 4. Execução do Sistema

O programa é compatível com múltiplos ambientes operacionais, incluindo a LinuxVM de avaliação.

#### No ambiente Windows (PowerShell):
```bash
\$env:PYTHONPATH="src"; py src/principal.py
```

#### No ambiente Linux / macOS (Terminal):
```bash
PYTHONPATH=src python3 src/principal.py
```

---

## Relatórios Estatísticos Implementados
Conforme as especificações do Item 6 do edital, o sistema conta com dois relatórios automatizados via leitura de arquivos SQL externos:
1. Contagem de Recursos por Situação: Consulta estruturada com cláusula GROUP BY para sumarização quantitativa do estado dos recursos cadastrados.
2. Relatório Detalhado de Acessibilidade: Consulta baseada em INNER JOIN para o cruzamento de dados relacionais entre estabelecimentos e recursos vinculados.

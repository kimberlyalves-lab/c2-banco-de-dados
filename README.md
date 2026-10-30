# Sistema de Controle de Acessibilidade e Recursos (acessibilidade)

Este projeto foi desenvolvido como parte da disciplina de Banco de Dados. O objetivo da aplicação é simular a interface entre uma linguagem de programação e o banco de dados MySQL, permitindo gerenciar locais e seus respectivos recursos de acessibilidade de forma eficiente.

## Integrantes do Grupo
* Kimberly Alves dos Santos - 25110020

**Professor:** Howard Roatti  
**Disciplina:** Banco de Dados  
**Semestre:** 2026/2  

---

## Tecnologias Utilizadas
* **Banco de Dados:** MySQL 8.0 (Engine InnoDB)
* **Modelagem:** MySQL Workbench
* **Linguagem de Programação:** Python

---

## Estrutura do Banco de Dados 

O banco de dados `acessibilidade` é composto por duas tabelas principais relacionadas de forma não-identificadora, garantindo a integridade referencial:

1. **locais:** Armazena os estabelecimentos ou locais mapeados (`id_local`, `nome`, `tipo`, `endereco`, `cidade`).
2. **recursos:** Armazena os recursos de acessibilidade vinculados a cada local (`id_recurso`, `id_local`, `nome`, `tipo_deficiencia`, `situacao`, `data_verificacao`).

O script inclui uma restrição do tipo `CHECK` (`chk_situacao`) para garantir que o estado de um recurso seja estritamente: `FUNCIONANDO`, `EM MANUTENCAO` ou `INEXISTENTE`.

---

## Como Executar o Script de Banco de Dados

### Configurar o Banco de Dados
Acesse o seu ambiente MySQL Workbench ou terminal MySQL e execute o script disponível na raiz do projeto:
```sql
-- Executar o arquivo tabelas_criacao.sql completo para gerar a estrutura testada.
```

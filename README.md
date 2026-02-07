# 🚀 FinAssist Pro 2

> **O Assistente Financeiro Inteligente, Privado e 100% Offline.**

Bem-vindo ao **FinAssist Pro 2**, a evolução definitiva do projeto FinAssist. Esta versão foi reescrita do zero utilizando uma arquitetura modular baseada em serviços, interface conversacional moderna via **Chainlit** e inteligência artificial local via **Ollama**.

---

## Funcionalidades Principais

* Multiplataforma: Interface Web via Chainlit e aplicação nativa Desktop para Windows via Flet.

* Processamento de Linguagem Natural: Registro inteligente de transações (ex: "Gastei 50 reais na padaria").

* Privacidade Offline: Integração com Ollama (Llama 3) rodando 100% local.

* Gestão Financeira: Acompanhamento de saldo em tempo real e progresso de metas ativas.

---

## Stack Tecnológica

O projeto segue padrões rígidos de Engenharia de Software:

* **Linguagem:** Python 3.12+
* **Interface:** Web: Chainlit / Desktop: Flet.
* **Banco de Dados:** SQLite (via `aiosqlite` + SQLAlchemy 2.0 Async)
* **IA / LLM:** [Ollama](https://ollama.com/) (Localhost)
* **Modelo Padrão:** `llama3:8b` (Configurado com temperatura 0.1 para precisão matemática)

---
## Instalação e Uso

Pré-requisitos

1. Python 3.10 ou superior.

2. Ollama instalado e rodando em sua máquina.

3. Modelo Llama 3 baixado no Ollama:
```bash
ollama pull llama3:8b
```
## Exemplos de Comandos

  O FinAssist Pro 2 entende linguagem natural. Tente enviar mensagens como:

1. Registrar Gastos:
  
  "Gastei 45 reais na padaria hoje de manhã." "Paguei 120 de conta de luz."
  
2. Registrar Ganhos:

  "Recebi 2500 de salário."

3. Consultas:

  "Qual é o meu saldo atual?" "Resuma minhas últimas transações."

4. Metas:

  "Quero criar uma meta de viajar para a praia, preciso de 3000 reais até dezembro."

## Privacidade e Segurança

Todas as interações são processadas pelo Controller de IA localmente.

- Zero Nuvem: Nenhuma transação é enviada para APIs da OpenAI ou Anthropic.

- Persistência Local: O banco de dados (finassist.db) e o perfil de usuário são salvos na pasta data/ dentro do projeto.

## Contribuição

Contribuições são bem-vindas! Por favor, siga o padrão de Pull Requests e mantenha a arquitetura de repositórios ao adicionar novas funcionalidades.

Desenvolvido por Maurício Rafael de Souza Osuna



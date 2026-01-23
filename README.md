# 🚀 FinAssist Pro 2

> **O Assistente Financeiro Inteligente, Privado e 100% Offline.**

Bem-vindo ao **FinAssist Pro 2**, a evolução definitiva do projeto FinAssist. Esta versão foi reescrita do zero utilizando uma arquitetura modular baseada em serviços, interface conversacional moderna via **Chainlit** e inteligência artificial local via **Ollama**.

---

## O que há de novo na v2?

Diferente da versão anterior, o FinAssist Pro 2 foca em privacidade total e performance assíncrona:

* **Arquitetura "Offline-First":** Seus dados financeiros nunca saem da sua máquina. A IA roda localmente.
* **Interface via Chat (Chainlit):** Interaja com suas finanças como se estivesse conversando com um mentor no WhatsApp/Telegram.
* **Ações Autônomas:** A IA não apenas responde, ela executa ações (registra gastos, cria metas) diretamente no banco de dados via *Function Calling* simulado.
* **Stack Robusta:** Python 3.12+, SQLAlchemy (Async), Pydantic e Llama 3.

---

## Stack Tecnológica

O projeto segue padrões rígidos de Engenharia de Software:

* **Linguagem:** Python 3.12+
* **Interface:** [Chainlit](https://docs.chainlit.io) (Frontend conversacional)
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



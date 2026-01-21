import sys
import os

# --- CORREÇÃO DE PATH (Adicione este bloco no topo) ---
# Isso garante que o Python encontre a pasta 'src' mesmo rodando de dentro dela
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(root_dir)
# -----------------------------------------------------

import json
import chainlit as cl
from src.core.database import get_db
from src.ai.controller import AIController

# Configuração de Caminhos
DATA_DIR = os.path.join(root_dir, "data")
PROFILE_PATH = os.path.join(DATA_DIR, "perfil_investidor.json")

async def load_profile_name():
    """Lê o nome do usuário do arquivo JSON legado/simples."""
    if os.path.exists(PROFILE_PATH):
        try:
            with open(PROFILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("nome", "Investidor")
        except:
            return "Investidor"
    return None

async def save_profile_name(nome):
    """Salva o nome para as próximas sessões."""
    os.makedirs(DATA_DIR, exist_ok=True)
    data = {"nome": nome, "perfil": "Moderado"} # Default
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@cl.on_chat_start
async def start():
    # 1. Onboarding
    nome_usuario = await load_profile_name()
    
    if not nome_usuario:
        await cl.Message(content="👋 Olá! Bem-vindo ao **FinAssist Pro 2**.\nSou seu mentor financeiro pessoal e 100% offline.").send()
        res = await cl.AskUserMessage(content="Como você gostaria de ser chamado?", timeout=60).send()
        if res:
            nome_usuario = res.get("output", "Investidor")
            await save_profile_name(nome_usuario)
            await cl.Message(content=f"Prazer, **{nome_usuario}**! Configurando seu banco de dados seguro...").send()
    else:
        await cl.Message(content=f"👋 Bem-vindo de volta, **{nome_usuario}**!").send()

    # 2. Mensagem inicial
    await cl.Message(content="O sistema está pronto. Você pode me dizer seus gastos, perguntar saldo ou criar metas.\n\n*Ex: 'Gastei 50 reais na padaria' ou 'Qual meu saldo?'*").send()

@cl.on_message
async def main(message: cl.Message):
    async for session in get_db():
        controller = AIController(session)
        
        msg = cl.Message(content="")
        await msg.send()
        
        response = await controller.process_query(message.content)
        
        msg.content = response
        await msg.update()
        break
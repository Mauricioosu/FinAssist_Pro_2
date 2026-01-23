import sys
import os
import json
import chainlit as cl
import aiofiles

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(root_dir)

from src.core.database import get_db, init_db
from src.ai.controller import AIController


DATA_DIR = os.path.join(root_dir, "data")
PROFILE_PATH = os.path.join(DATA_DIR, "perfil_investidor.json")


async def load_profile_name():
    """
    Lê o nome do usuário do arquivo JSON de forma 100% assíncrona.
    Isso evita bloquear o event loop durante a leitura do disco.
    """
    if os.path.exists(PROFILE_PATH):
        try:
            # Refatorado: Uso de aiofiles para leitura não bloqueante
            async with aiofiles.open(PROFILE_PATH, "r", encoding="utf-8") as f:
                content = await f.read()
                data = json.loads(content)
                return data.get("nome", "Investidor")
        except Exception:
            # Em caso de erro de leitura ou JSON inválido, retorna padrão
            return "Investidor"
    return None


async def save_profile_name(nome):
    """
    Salva o nome para as próximas sessões de forma assíncrona.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    data = {"nome": nome, "perfil": "Moderado"}
    async with aiofiles.open(PROFILE_PATH, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=4))


@cl.on_chat_start
async def start():
    # Inicialização do banco de dados
    await init_db()
    # Carregar ou solicitar o nome do usuário
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

    # Mensagem inicial
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

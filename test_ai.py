import asyncio
from src.core.database import get_db
from src.ai.controller import AIController

async def main():
    print("--- TESTE DE IA + BANCO DE DADOS ---")
    
    async for session in get_db():
        controller = AIController(session)
        
        # Cenário 1: Pergunta de Leitura
        print("\nUSER: Qual é o meu saldo atual?")
        resp = await controller.process_query("Qual é o meu saldo atual e o que eu gastei recentemente?")
        print(f"IA: {resp}")
        
        # Cenário 2: Comando de Escrita
        print("\nUSER: Gastei 150 reais no mercado agora.")
        resp = await controller.process_query("Gastei 150 reais no mercado agora, categoria Alimentação.")
        print(f"IA: {resp}")
        
        # Cenário 3: Confirmação (Leitura pós-escrita)
        print("\nUSER: Como ficou meu saldo?")
        resp = await controller.process_query("Como ficou meu saldo?")
        print(f"IA: {resp}")
        
        break

if __name__ == "__main__":
    asyncio.run(main())
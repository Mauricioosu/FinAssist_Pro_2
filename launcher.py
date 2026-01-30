import os
import sys
import time
import subprocess
import requests
import shutil
from tqdm import tqdm
from chainlit.cli import run_chainlit

# CONFIGURAÇÕES
OLLAMA_INSTALLER_URL = "https://ollama.com/download/OllamaSetup.exe"
MODEL_NAME = "llama3:8b"


def is_ollama_installed():
    """Verifica se o comando 'ollama' existe no sistema."""
    return shutil.which("ollama") is not None


def is_server_running():
    """Tenta conectar no servidor local do Ollama."""
    try:
        response = requests.get("http://localhost:11434", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def download_file(url, filename):
    """Baixa um arquivo com barra de progresso."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    print(f"⬇️ Baixando {filename} de fonte oficial...")
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)


def install_ollama():
    """Baixa e inicia o instalador do Ollama."""
    installer_name = "OllamaSetup.exe"

    if not os.path.exists(installer_name):
        try:
            download_file(OLLAMA_INSTALLER_URL, installer_name)
        except Exception as e:
            print(f"❌ Erro ao baixar Ollama: {e}")
            input("Pressione Enter para sair...")
            sys.exit(1)

    print("\n🚀 Iniciando instalador do Ollama...")
    print("⚠️ POR FAVOR, complete a instalação na janela que abrir e depois volte aqui!")

    # Roda o instalador e espera
    subprocess.run([installer_name], check=True)

    print("⏳ Verificando instalação...")
    time.sleep(5)

    if not is_ollama_installed():
        print("❌ Parece que o Ollama não foi instalado ou o PC precisa reiniciar.")
        print("Tente reiniciar o computador e abrir este programa novamente.")
        input("Pressione Enter para sair...")
        sys.exit(1)

    try:
        os.remove(installer_name)
    except Exception:
        pass


def check_and_pull_model():
    """Garante que o modelo de IA esteja baixado."""
    print(f"🧠 Verificando modelo de IA ({MODEL_NAME})...")

    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, encoding='utf-8')
        if MODEL_NAME in result.stdout:
            print("✅ Modelo IA já está pronto.")
            return
    except Exception:
        pass

    print(f"⚡ Baixando a Inteligência Artificial ({MODEL_NAME}). Isso pode demorar uns minutos...")
    try:
        process = subprocess.Popen(["ollama", "pull", MODEL_NAME], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        print("✅ Download da IA concluído!")
    except Exception as e:
        print(f"❌ Erro ao baixar modelo: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)


def main():
    print("==========================================")
    print("   💰 BEM-VINDO AO FINASSIST PRO 2 💰")
    print("==========================================\n")

    # Verifica Instalação do Ollama
    if not is_ollama_installed():
        print("⚠️ O motor de IA (Ollama) não foi encontrado.")
        print("Vamos instalá-lo automaticamente para você.")
        install_ollama()

    # Garante que o servidor esteja rodando
    if not is_server_running():
        print("🔄 Iniciando servidor de IA em background...")
        subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(5)

    # Verifica e Baixa o Modelo (Llama 3)
    check_and_pull_model()

    # Inicia o App
    print("\n🌟 TUDO PRONTO! Abrindo seu Assistente Financeiro...")

    # Configurações do Chainlit
    os.environ["CHAINLIT_HEADLESS"] = "true"
    os.environ["CHAINLIT_PORT"] = "8000"

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    target_app = os.path.join(base_path, "src", "app.py")
    sys.argv = ["chainlit", "run", target_app]
    run_chainlit(sys.argv[0])


if __name__ == "__main__":
    main()

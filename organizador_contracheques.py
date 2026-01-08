import os
import re
import shutil
import pdfplumber


# ================= CONFIGURAÇÕES =================

# Padrão final de nome:
# ANO-MÊS - CC - TIPO.pdf
#
# Exemplos:
# 2025-09 - CC - Normal.pdf
# 2025-12 - CC - 13Salario.pdf


# ================= FUNÇÕES =================

def extrair_tipo_folha(caminho_pdf):
    """
    Extrai o valor do campo 'Tipo da Folha' do PDF.
    Retorna uma string ou None.
    """
    try:
        texto = ""
        with pdfplumber.open(caminho_pdf) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    texto += page_text + "\n"
    except Exception:
        return None

    match = re.search(r"(?i)Tipo da Folha\s*[:\-–—]?\s*(.+)", texto)
    if match:
        return match.group(1).splitlines()[0].strip()

    return None


def extrair_ano_mes(texto):
    """
    Extrai mês e ano no formato MM/YYYY ou M/YYYY.
    Retorna (ano, mes) com mês sempre em 2 dígitos.
    """
    match = re.search(r"(\b\d{1,2})/(\d{4}\b)", texto)
    if not match:
        return None, None

    mes = match.group(1).zfill(2)
    ano = match.group(2)
    return ano, mes


def normalizar_tipo_folha(texto):
    """
    Normaliza o tipo da folha para o padrão final.
    """
    t = texto.upper()

    if "13" in t:
        return "13Salario"
    if "FERIA" in t:
        return "Ferias"

    return "Normal"


def gerar_nome_unico(pasta, nome):
    """
    Evita sobrescrever arquivos existentes.
    """
    caminho = os.path.join(pasta, nome)
    if not os.path.exists(caminho):
        return caminho

    base, ext = os.path.splitext(nome)
    contador = 1
    while True:
        novo_nome = f"{base}_{contador}{ext}"
        novo_caminho = os.path.join(pasta, novo_nome)
        if not os.path.exists(novo_caminho):
            return novo_caminho
        contador += 1


def processar_pasta(pasta_origem):
    """
    Processa todos os PDFs da pasta:
    - extrai informações
    - renomeia
    - move para subpasta do ano
    """
    arquivos = [f for f in os.listdir(pasta_origem) if f.lower().endswith(".pdf")]

    if not arquivos:
        print("Nenhum PDF encontrado na pasta.")
        return

    for arquivo in arquivos:
        caminho_atual = os.path.join(pasta_origem, arquivo)
        print(f"Processando: {arquivo}")

        tipo_folha = extrair_tipo_folha(caminho_atual)
        if not tipo_folha:
            print("  ❌ Tipo da Folha não encontrado.")
            continue

        ano, mes = extrair_ano_mes(tipo_folha)
        if not ano or not mes:
            print("  ❌ Data (MM/YYYY) não encontrada.")
            continue

        tipo_normalizado = normalizar_tipo_folha(tipo_folha)

        nome_novo = f"{ano}-{mes} - CC - {tipo_normalizado}.pdf"

        pasta_ano = os.path.join(pasta_origem, ano)
        os.makedirs(pasta_ano, exist_ok=True)

        destino = gerar_nome_unico(pasta_ano, nome_novo)

        try:
            shutil.move(caminho_atual, destino)
            print(f"  ✅ Movido para: {os.path.relpath(destino, pasta_origem)}")
        except Exception as e:
            print(f"  ❌ Erro ao mover arquivo: {e}")

    print("\n✔ Processamento finalizado.")


# ================= EXECUÇÃO =================

if __name__ == "__main__":
    pasta = input("Informe o caminho da pasta com os PDFs: ").strip()

    if not pasta or not os.path.isdir(pasta):
        print("Caminho inválido.")
    else:
        processar_pasta(pasta)

    input("\nPressione ENTER para sair...")

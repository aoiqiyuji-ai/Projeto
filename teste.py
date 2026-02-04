import requests
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import textwrap
from urllib.parse import quote

def criar_pdf(texto, nome_arquivo):
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4
    linhas = textwrap.wrap(texto, width=90)
    y = altura - 50

    for linha in linhas:
        c.drawString(50, y, linha)
        y -= 15
        if y < 50:
            c.showPage()
            y = altura - 50

    c.save()

def pegar_conteudo_wikipedia(tema):
    base_url = "https://en.wikipedia.org/wiki/"
    url = base_url + quote(tema)

    # Cabeçalhos para parecer navegador e reduzir chance de bloqueio
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        resposta.raise_for_status()  # garante que página existe

        soup = BeautifulSoup(resposta.text, "html.parser")
        paragrafos = soup.find_all("p")
        texto = ""

        if not paragrafos:
            print("Nenhum conteúdo encontrado nessa página.")
            return None

        for p in paragrafos[:5]:
            texto += p.get_text().strip() + "\n\n"

        return texto

    except requests.exceptions.RequestException as erro:
        print("Erro ao acessar a página. Pode ser tema incorreto ou problema de rede:")
        print(erro)
        return None

# --- Programa principal ---
tema = input("Digite o tema que deseja estudar: ")

# Para teste seguro, você pode digitar "Cat" ou "Python_(programming_language)"
conteudo = pegar_conteudo_wikipedia(tema)

if conteudo:
    nome_pdf = tema.replace(" ", "_") + ".pdf"
    criar_pdf(conteudo, nome_pdf)
    print(f"PDF criado com sucesso: {nome_pdf}")
else:
    print("Não foi possível gerar o PDF.")
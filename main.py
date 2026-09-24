import os
import xml.etree.ElementTree as ET
import http.server
import socketserver
import threading
import time
import requests

# ⚙️ SUAS CONFIGURAÇÕES FIXAS E SEGURAS
TOKEN_TELEGRAM = "8916517622:AAG-GiHzq0nz3oEPS8v96eV5GXVN2cqXSMQ"
CHAT_ID = "1072159736"

PRODUTOS_DESEJADOS = [
    "umbro",
    "pro 5",
    "bump",
    "topper",
    "lethal",
    "grafeno",
    "geladeira",
    "electrolux",
    "tf71",
    "brm62",
    "brastemp",
    "tcl",
    "50c6",
    "55c6",
    "qled",
    "playstation",
    "ps5",
    "cupom",
    "desconto",
    "shopee",
    "amazon",
    "magalu",
    "mercado livre",
    "kabum",
]


# 🌐 SISTEMA DE SEGURANÇA PARA MANTER O SERVIDOR GRÁTIS LIGADO
def iniciar_servidor_web():
    """Cria uma página web falsa para o Render não desligar o robô grátis"""
    porta = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", porta), handler) as httpd:
        httpd.serve_forever()


# Liga a página falsa em segundo plano
threading.Thread(target=iniciar_servidor_web, daemon=True).start()


def enviar_alerta_telegram(titulo, link):
    url_send = f"https://telegram.org{TOKEN_TELEGRAM}/sendMessage"
    mensagem = f"🔥 *ALERTA DE MONITORAMENTO!* 🔥\n\n📦 *Item:* {titulo}\n\n👉 *Link:* {link}"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url_send, json=payload, timeout=5)
    except:
        pass


alertas_enviados = []
URL_FEED_AGREGADOR = "https://promobit.com.br"

print("🧙‍♂️ MONITOR MULTILOJAS GRATUITO ATIVADO!")

while True:
    try:
        response = requests.get(
            URL_FEED_AGREGADOR,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            },
            timeout=10,
        )
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall(".//item")[:20]:
                titulo = item.find("title").text
                link = item.find("link").text
                id_oferta = (
                    item.find("guid").text
                    if item.find("guid") is not None
                    else link
                )

                if id_oferta not in alertas_enviados:
                    titulo_minusculo = titulo.lower()
                    achou_produto = any(
                        termo in titulo_minusculo for termo in PRODUTOS_DESEJADOS
                    )
                    if achou_produto:
                        enviar_alerta_telegram(titulo, link)
                    alertas_enviados.append(id_oferta)
    except:
        pass
    time.sleep(15)


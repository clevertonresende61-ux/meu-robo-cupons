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

# Lista de desejos expandida com termos abrangentes para garantir que o robô encontre ofertas
PRODUTOS_DESEJADOS = [
    "umbro", "pro 5", "bump", "topper", "lethal", "grafeno", 
    "geladeira", "electrolux", "tf71", "brm62", "brastemp", 
    "tcl", "50c6", "55c6", "qled", "playstation", "ps5", 
    "cupom", "desconto", "shopee", "amazon", "magalu", 
    "mercado livre", "kabum", "promocao", "oferta", "gratis"
]

# 🌐 SISTEMA DE SEGURANÇA PARA MANTER O SERVIDOR GRÁTIS LIGADO
def iniciar_servidor_web():
    porta = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", porta), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=iniciar_servidor_web, daemon=True).start()

def enviar_alerta_telegram(titulo, link, tipo="🔥 ALERTA"):
    url_send = f"https://telegram.org{TOKEN_TELEGRAM}/sendMessage"
    mensagem = f"{tipo}!\n\n📦 *Item:* {titulo}\n\n👉 *Link:* {link}"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url_send, json=payload, timeout=5)
    except:
        pass

# Envia uma mensagem inicial para você ter certeza absoluta que o robô ligou
enviar_alerta_telegram("O robô foi atualizado e está caçando cupons na nuvem agora!", "https://shopee.com.br", "🧙‍♂️ BRUXÃO INFORMA")

alertas_enviados = []

# Fontes alternativas livres de bloqueio (Agregador de Ofertas + Google News Promoções)
URLS_FEEDS = [
    "https://pelando.com.br",
    "https://google.com"
]

while True:
    for url in URLS_FEEDS:
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
                timeout=10
            )
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                for item in root.findall(".//item")[:15]:
                    titulo = item.find("title").text
                    link = item.find("link").text
                    id_oferta = item.find("guid").text if item.find("guid") is not None else link

                    if id_oferta not in alertas_enviados:
                        titulo_minusculo = titulo.lower()
                        
                        # Verifica se possui algum dos seus produtos ou termos de cupom
                        achou_produto = any(termo in titulo_minusculo for termo in PRODUTOS_DESEJADOS)
                        
                        if achou_produto:
                            enviar_alerta_telegram(titulo, link)
                            
                        alertas_enviados.append(id_oferta)
        except Exception as e:
            print(f"Erro ao ler feed: {e}")
            
    # Checa a cada 20 segundos para manter alta velocidade sem derrubar a conexão
    time.sleep(20)



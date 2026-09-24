import os
import xml.etree.ElementTree as ET
import http.server
import socketserver
import threading
import time
import requests
import telebot  # Usando o sistema oficial que funcionou!

# ⚙️ CONFIGURAÇÕES FIXAS E SEGURAS
TOKEN_TELEGRAM = "8916517622:AAG-GiHzq0nz3oEPS8v96eV5GXVN2cqXSMQ"
CHAT_ID = "1072159736"

# Inicializa o bot oficial
bot = telebot.TeleBot(TOKEN_TELEGRAM)

# Lista de desejos de produtos e cupons
PRODUTOS_DESEJADOS = [
    "umbro", "pro 5", "bump", "topper", "lethal", "grafeno", 
    "geladeira", "electrolux", "tf71", "brm62", "brastemp", 
    "tcl", "50c6", "55c6", "qled", "playstation", "ps5", 
    "cupom", "desconto", "shopee", "amazon", "magalu", 
    "mercado livre", "kabum", "promocao", "oferta"
]

# 🌐 SISTEMA PARA MANTER O SERVIDOR GRÁTIS LIGADO
def iniciar_servidor_web():
    porta = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", porta), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=iniciar_servidor_web, daemon=True).start()

# Mensagem de inicialização para você saber que a nuvem ativou
try:
    bot.send_message(CHAT_ID, "🧙‍♂️ BRUXÃO INFORMA: Monitor na nuvem ATIVADO e caçando cupons!")
except:
    pass

alertas_enviados = []

# Canais de Feeds Globais de Ofertas e Cupons
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
                        
                        # Filtro inteligente
                        achou_produto = any(termo in titulo_minusculo for termo in PRODUTOS_DESEJADOS)
                        
                        if achou_produto:
                            mensagem = f"🔥 *ALERTA DE PROMOÇÃO!* 🔥\n\n📦 *Item:* {titulo}\n\n👉 *Link:* {link}"
                            bot.send_message(CHAT_ID, mensaje, parse_mode="Markdown")
                            
                        alertas_enviados.append(id_oferta)
        except:
            pass
            
    # Varre a internet a cada 20 segundos
    time.sleep(20)




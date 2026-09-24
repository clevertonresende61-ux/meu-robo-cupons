import os
import xml.etree.ElementTree as ET
import http.server
import socketserver
import threading
import time
import requests
import telebot

# ⚙️ CONFIGURAÇÕES FIXAS E SEGURAS
TOKEN_TELEGRAM = "8916517622:AAG-GiHzq0nz3oEPS8v96eV5GXVN2cqXSMQ"
CHAT_ID = "1072159736"

bot = telebot.TeleBot(TOKEN_TELEGRAM)

def iniciar_servidor_web():
    porta = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", porta), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=iniciar_servidor_web, daemon=True).start()

# Aviso direto
bot.send_message(CHAT_ID, "⚡ SISTEMA FINAL ATIVADO: Buscando cupons e ofertas no banco de dados aberto do Google!")

alertas_enviados = []

# Rota direta do Google News RSS focada em promoções brasileiras
URL_DADO_ABERTO = "https://google.com"

while True:
    try:
        response = requests.get(
            URL_DADO_ABERTO,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            timeout=10
        )
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            itens = root.findall(".//item")
            
            # Varre os últimos 20 lançamentos e ofertas registrados
            for item in itens[:20]:
                titulo = item.find("title").text
                link = item.find("link").text
                id_oferta = item.find("guid").text if item.find("guid") is not None else link

                if id_oferta not in alertas_enviados:
                    # Envia tudo o que encontrar na rede sem nenhum filtro de palavra específica
                    mensagem = f"🔥 *OFERTA / NOTÍCIA ENCONTRADA!* 🔥\n\n📦 *Item:* {titulo}\n\n👉 *Link:* {link}"
                    bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
                    alertas_enviados.append(id_oferta)
                    
    except Exception as e:
        pass

    # Varre a rede a cada 30 segundos de forma limpa e contínua
    time.sleep(30)







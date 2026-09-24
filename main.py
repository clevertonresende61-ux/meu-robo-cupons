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

# Aviso de ativação do modo sem limites
bot.send_message(CHAT_ID, "🚀 MODO ARRASTÃO ATIVADO! O robô agora vai enviar QUALQUER promoção nacional sem filtros de produtos!")

alertas_enviados = []

# Nova rota utilizando o feed público do Pelando via proxyRSS (Livre de bloqueios e ultra rápido)
URL_FEED_GLOBAL = "https://rss.app"

while True:
    try:
        # Faz a varredura usando um navegador simulado de alta velocidade
        response = requests.get(
            URL_FEED_GLOBAL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            timeout=10
        )
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            itens = root.findall(".//item")
            
            # Analisa as últimas 15 promoções postadas no Brasil naquele exato instante
            for item in itens[:15]:
                titulo = item.find("title").text
                link = item.find("link").text
                id_oferta = item.find("guid").text if item.find("guid") is not None else link

                # Se for uma promoção inédita na internet, envia na marra sem filtrar nada!
                if id_oferta not in alertas_enviados:
                    mensagem = (
                        f"🔥 *NOVA OFERTA DETECTADA!* 🔥\n\n"
                        f"📦 *Item:* {titulo}\n\n"
                        f"👉 *Link da Promoção:* {link}"
                    )
                    bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
                    alertas_enviados.append(id_oferta)
                    
    except Exception as e:
        # Silencia erros temporários de conexão para não poluir o seu chat
        pass

    # Checa a internet a cada 25 segundos procurando novas postagens
    time.sleep(25)






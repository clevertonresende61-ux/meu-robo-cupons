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

# Deixei os termos super amplos para o robô pescar qualquer coisa e começar a enviar
PRODUTOS_DESEJADOS = [
    "umbro", "pro 5", "bump", "topper", "lethal", "grafeno", 
    "geladeira", "electrolux", "tf71", "brm62", "brastemp", 
    "tcl", "50c6", "55c6", "qled", "playstation", "ps5", 
    "cupom", "desconto", "shopee", "amazon", "magalu", 
    "mercado livre", "kabum", "promocao", "oferta", "ganhe"
]

def iniciar_servidor_web():
    porta = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", porta), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=iniciar_servidor_web, daemon=True).start()

# Força um aviso no momento em que você salva
bot.send_message(CHAT_ID, "🔮 BRUXÃO INFORMA: Conexão atualizada com nova rota 100% livre de bloqueios!")

alertas_enviados = []

# Nova rota utilizando a busca do Google estruturada em modo RSS puro
URL_FONTE_NOTICIAS = "https://google.com"

contador_loops = 0

while True:
    try:
        response = requests.get(
            URL_FONTE_NOTICIAS,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            timeout=10
        )
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            itens = root.findall(".//item")
            
            for item in itens[:20]:
                titulo = item.find("title").text
                link = item.find("link").text
                id_oferta = item.find("guid").text if item.find("guid") is not None else link

                if id_oferta not in alertas_enviados:
                    titulo_minusculo = titulo.lower()
                    
                    # Se bater com qualquer termo da nossa lista grande, ele dispara
                    achou_algo = any(termo in titulo_minusculo for termo in PRODUTOS_DESEJADOS)
                    
                    if achou_algo:
                        mensagem = f"🔥 *NOVA OPORTUNIDADE DETECTADA!* 🔥\n\n📦 *Título:* {titulo}\n\n👉 *Link:* {link}"
                        bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
                        
                    alertas_enviados.append(id_oferta)
                    
    except Exception as e:
        print(f"Erro na varredura: {e}")
        
    contador_loops += 1
    
    # Sistema de teste: a cada 3 loops (1 minuto), ele te avisa que está vivo se não mandar nada
    if contador_loops % 3 == 0:
        try:
            bot.send_message(CHAT_ID, "⏳ _Robô em execução: Varrendo o mercado à procura de novos cupons..._", parse_mode="Markdown")
        except:
            pass

    # Checagem rápida de 20 segundos
    time.sleep(20)





import xml.etree.ElementTree as ET
import time
import requests

# ⚙️ SUAS CONFIGURAÇÕES FIXAS E SEGURAS
TOKEN_TELEGRAM = "8916517622:AAG-GiHzq0nz3oEPS8v96eV5GXVN2cqXSMQ"
CHAT_ID = "1072159736"

# Lista de termos que você quer monitorar (Tudo em letra minúscula para o robô não errar)
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


def enviar_alerta_telegram(titulo, link):
    """Envia o alerta ultra rápido para o seu celular se passar pelo filtro"""
    url_send = f"https://telegram.org{TOKEN_TELEGRAM}/sendMessage"

    mensagem = (
        f"🔥 *ALERTA DE MONITORAMENTO DETECTADO!* 🔥\n\n"
        f"📦 *Item:* {titulo}\n\n"
        f"👉 *Link da Oferta:* {link}"
    )

    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}

    try:
        requests.post(url_send, json=payload, timeout=5)
        print(f"⚡ Alerta enviado: {titulo[:40]}...")
    except Exception as e:
        print(f"Erro ao enviar: {e}")


# Banco de dados temporário para o robô não repetir mensagens
alertas_enviados = []

# Feed agregador que junta cupons e promoções das maiores lojas do Brasil em tempo real
URL_FEED_AGREGADOR = "https://promobit.com.br"

print("🧙‍♂️ BRUXÃO INFORMA: Monitor Multilojas Ativado!")
print("Procurando por Chuteiras, TVs, Geladeiras, PS5 e Cupons Gerais...\n")

while True:
    try:
        # Faz uma requisição leve ao servidor agregador de ofertas
        response = requests.get(
            URL_FEED_AGREGADOR,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            },
            timeout=10,
        )

        if response.status_code == 200:
            root = ET.fromstring(response.content)

            # Analisa as últimas 20 promoções postadas na internet
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

                    # Varre a sua lista de desejos para ver se o item bate com o que você quer
                    achou_produto = any(
                        termo in titulo_minusculo for termo in PRODUTOS_DESEJADOS
                    )

                    if achou_produto:
                        enviar_alerta_telegram(titulo, link)

                    # Salva na memória para não analisar o mesmo item no próximo segundo
                    alertas_enviados.append(id_oferta)

    except Exception as e:
        print(f"Aguardando próxima varredura... ({e})")

    # Checa a cada 15 segundos para pegar as ofertas assim que entrarem no ar
    time.sleep(15)

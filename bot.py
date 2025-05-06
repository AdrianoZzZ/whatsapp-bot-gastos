from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'gastos.csv'

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=['data', 'categoria', 'valor']).to_csv(DATA_FILE, index=False)

def registrar_gasto(msg):
    match = re.search(r'gastei\s*R?\$?\s*([\d,\.]+)\s*(com|em)?\s*(\w+)', msg, re.IGNORECASE)
    if match:
        valor_str, _, categoria = match.groups()
        valor = float(valor_str.replace(',', '.'))
        data_hoje = datetime.now().strftime('%Y-%m-%d')
        df = pd.read_csv(DATA_FILE)
        df = df.append({'data': data_hoje, 'categoria': categoria.lower(), 'valor': valor}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        return f"Gasto de R$ {valor:.2f} em '{categoria}' registrado!"
    return "Não entendi seu gasto. Tente algo como: 'Gastei 50 com transporte'."

def gerar_resumo():
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        return "Nenhum gasto registrado ainda."
    total = df['valor'].sum()
    top = df.groupby('categoria')['valor'].sum().sort_values(ascending=False).head(3)
    texto = f"Total gasto: R$ {total:.2f}\nPrincipais categorias:\n"
    for cat, val in top.items():
        texto += f"- {cat.title()}: R$ {val:.2f}\n"
    return texto

def gerar_grafico():
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        return None
    resumo = df.groupby('categoria')['valor'].sum()
    plt.figure(figsize=(6,4))
    resumo.plot(kind='bar', color='mediumseagreen')
    plt.title('Gastos por Categoria')
    plt.ylabel('R$')
    plt.tight_layout()
    nome_arquivo = 'static/grafico.png'
    plt.savefig(nome_arquivo)
    plt.close()
    return nome_arquivo

@app.route('/whatsapp', methods=['POST'])
def whatsapp_bot():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    
    if msg.lower().startswith('gastei'):
        resposta = registrar_gasto(msg)
    elif 'resumo' in msg.lower():
        resposta = gerar_resumo()
    elif 'gráfico' in msg.lower() or 'grafico' in msg.lower():
        caminho = gerar_grafico()
        if caminho:
            msg_resp = resp.message("Aqui está seu gráfico de gastos:")
            msg_resp.media(request.url_root + caminho)
            return str(resp)
        else:
            resposta = "Nenhum dado para gerar gráfico."
    else:
        resposta = "Comandos disponíveis:\n- 'Gastei 50 com mercado'\n- 'Resumo'\n- 'Gráfico'"

    resp.message(resposta)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
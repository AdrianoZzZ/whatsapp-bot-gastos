# Bot de WhatsApp para Controle de Gastos

Este projeto é um bot inteligente para WhatsApp que permite registrar gastos, gerar gráficos e obter resumos financeiros via mensagens.

## Comandos disponíveis

- `Gastei 50 com mercado` – registra um gasto
- `Resumo` – mostra os principais gastos
- `Gráfico` – gera um gráfico dos gastos por categoria

## Como usar com Twilio + Render

1. Suba este projeto no GitHub
2. Crie um Web Service no [Render.com](https://render.com/)
3. Configure o webhook no Twilio:
   `https://seu-app-no-render.onrender.com/whatsapp`
4. Comece a enviar mensagens para o número do sandbox do Twilio
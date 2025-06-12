import os
import logging
import asyncio
import threading
from telegram import Update
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv
from TrojanBot.utils.distribution import Distribution
from TrojanBot.bot.telegram_bot import TelegramBot
from TrojanBot.config.logging_config import setup_logging
from contextlib import asynccontextmanager


setup_logging()
logger = logging.getLogger(__name__)
load_dotenv()
telegram_bot = TelegramBot()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    try:
        bot_app = await telegram_bot.run_setup()

        # 👇 Set Telegram webhook to your live/ngrok URL + path
        webhook_url = os.getenv("TELEGRAM_WEBHOOK_URL", "https://<your-url>/telegram")
        await bot_app.bot.set_webhook(url=webhook_url)
        logger.info("Application started successfully.")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def index():
    distribution_instance = Distribution()
    dist_tokens = distribution_instance.dist()
    cards_html = ""
    for token in dist_tokens:
        cards_html += f"""
        <div class="coin-card">
            <img src="{token['icon']}" alt="{token['symbol']} icon" class="coin-icon">
            <h2 class="coin-name">{token['name']}</h2>
            <h4 class="coin-description">{token['description']}</h4>
            <div class="coin-address"><strong>Address: </strong> {token['address']}</div>
            <div class="coin-symbol">({token['symbol']})</div>
            <div class="coin-detail"><strong>Chain:</strong> {token['chain']}</div>
            <div class="coin-detail"><strong>Price:</strong> ${token['price_usd']}</div>
            <div class="coin-detail"><strong>Market Cap:</strong> {token['market_cap']}</div>
            <div class="coin-detail"><strong>Liquidity:</strong> {token['liquidity']}</div>
            <div class="coin-detail"><strong>Volume:</strong> ${token['volume']}</div>
            <div class="coin-detail"><strong>Price Change:</strong> {token['price_change']}</div>
            <div class="coin-detail"><strong>Upside Score:</strong> {token['upside_score']}</div>
            <div class="coin-detail"><strong>Rug Score:</strong> {token['rug_score']}</div>
        </div>
        """

    html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Token Dashboard</title>
            <style>
                body {{
                    background: #f5f5f5;
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }}
                .grid {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    gap: 20px;
                }}
                .coin-card {{
                    background: white;
                    padding: 20px;
                    border-radius: 12px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                    width: 260px;
                    text-align: center;
                }}
                .coin-icon {{
                    width: 60px;
                    height: 60px;
                    object-fit: contain;
                    margin-bottom: 10px;
                }}
                .coin-name {{
                    font-size: 1.2rem;
                    font-weight: bold;
                    color: #333;
                    margin: 0;
                }}
                .coin-symbol {{
                    color: #666;
                    margin-bottom: 10px;
                }}
                .coin-detail {{
                    font-size: 0.95rem;
                    color: #444;
                    margin: 6px 0;
                }}
                .coin-address{{
                    word-break: break-all;
                }}
            </style>
        </head>
        <body>
            <h1 style="text-align:center;">Token Overview</h1>
            <div class="grid">
                {cards_html}
            </div>
        </body>
        </html>
    """
    return HTMLResponse(content=html_template)


@app.post("/telegram")
async def telegram_webhook(request: Request):
    try:
        try:
            data = await request.json()
        except Exception as e:
            return JSONResponse(content={"error": "Invalid JSON"}, status_code=400)

        if telegram_bot.app is None:
            return JSONResponse(content={"error": "Bot not initialized"}, status_code=500)

        update = Update.de_json(data, telegram_bot.app.bot)
        await telegram_bot.app.process_update(update)
        return JSONResponse(content={"status": "ok"})
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {e}")
        return {"ok": False, "error": str(e)}

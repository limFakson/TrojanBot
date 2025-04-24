import os

from flask import Flask, render_template_string
from dotenv import load_dotenv
from TrojanBot.utils.distribution import Distribution


def main():
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    distribution_instance = Distribution()

    @app.route("/")
    def index():
        dist_token = distribution_instance.dist()
        html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Token Dashboard</title>
                <style>
                    body {
                        background: #f5f5f5;
                        font-family: Arial, sans-serif;
                        padding: 20px;
                    }
                    .grid {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: center;
                        gap: 20px;
                    }
                    .coin-card {
                        background: white;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                        width: 260px;
                        text-align: center;
                    }
                    .coin-icon {
                        width: 60px;
                        height: 60px;
                        object-fit: contain;
                        margin-bottom: 10px;
                    }
                    .coin-name {
                        font-size: 1.2rem;
                        font-weight: bold;
                        color: #333;
                        margin: 0;
                    }
                    .coin-symbol {
                        color: #666;
                        margin-bottom: 10px;
                    }
                    .coin-detail {
                        font-size: 0.95rem;
                        color: #444;
                        margin: 6px 0;
                    }
                    .coin-address{
                        word-break: break-all;
                    }
                </style>
            </head>
            <body>
                <h1 style="text-align:center;">Token Overview</h1>
                <div class="grid">
                    {% for token in dist_tokens %}
                    <div class="coin-card">
                        <img src="{{ token.icon }}" alt="{{ token.symbol }} icon" class="coin-icon">
                        <h2 class="coin-name">{{ token.name }}</h2>
                        <h4 class="coin-description">{{ token.description }}</h4>
                        <div class="coin-address"><strong>Address: </strong> {{ token.address }}</div>
                        <div class="coin-symbol">({{ token.symbol }})</div>
                        <div class="coin-detail"><strong>Chain:</strong> {{ token.chain }}</div>
                        <div class="coin-detail"><strong>Price:</strong> ${{ token.price }}</div>
                        <div class="coin-detail"><strong>Market Cap:</strong> {{ token.marketCap }}</div>
                        <div class="coin-detail"><strong>Liquidity:</strong> {{ token.liquidity }}</div>
                        <div class="coin-detail"><strong>Volume:</strong> ${{ token.volume }}</div>
                        <div class="coin-detail"><strong>Price Change:</strong> {{ token.price_change }}</div>
                        <div class="coin-detail"><strong>Upside Score:</strong> {{ token.upside_score }}</div>
                        <div class="coin-detail"><strong>Rug Score:</strong> {{ token.rug_score }}</div>
                    </div>
                    {% endfor %}
                </div>
            </body>
            </html>
        """
        return render_template_string(html_template, dist_tokens=dist_token)

    app.run(debug=True)


if __name__ == "__main__":
    main()

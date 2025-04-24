import logging
import os

from dotenv import load_dotenv

from .data_formater import standardize_token, analyze_token
from ..services.pumpfun_service import fetch_pump_fun_tokens
from ..services.dexscreener_service import fetch_dexscreener_tokens
from ..services.rugcheck_service import fetch_rugcheck_score
from ..config.logging_config import setup_logging

logger = logging.getLogger(__name__)


class Distribution:
    def __init__(self):
        self.enviroment = dict()
        self.formated_tokens = []
        self.coin_token = []
        self.results = []

        # Load essential functions
        setup_logging()
        self.enviroments()

    def enviroments(self):
        REQUIRED_VARS = [
            "DEX_API_URL",
            "PUMPFUN_URL",
            "RUGCHECK_API_URL",
            # "TWITTER_API_KEY",
            # "TWITTER_API_SECRET",
            # "TWITTER_ACCESS_TOKEN",
            # "TWITTER_ACCESS_SECRET",
            # "TELEGRAM_BOT_TOKEN",
            # "TELEGRAM_CHAT_ID",
            # "GEMINI_API_KEY",
        ]

        """Load and validate environment variables"""
        load_dotenv()

        for var in REQUIRED_VARS:
            value = os.getenv(var)
            if not value:
                logger.error(f"Missing required environment variable: {var}")
                raise ValueError(f"Missing required environment variable: {var}")
            self.enviroment[var] = value

    def dist(self):
        # Fetch tokens from both sources.
        pump_tokens = fetch_pump_fun_tokens(self.enviroment["PUMPFUN_URL"])
        dexscreener_tokens = fetch_dexscreener_tokens(self.enviroment["DEX_API_URL"])

        # Combine tokens from both sources.
        all_tokens_raw = pump_tokens + dexscreener_tokens
        standardized_tokens = []

        # Standardize each token's data so that we can work with a uniform structure.
        for token in all_tokens_raw:
            source = token.get("source", "")
            std_token = standardize_token(token, source)
            standardized_tokens.append(std_token)

        # Filter for Solana-based tokens.
        solana_tokens = []
        for token in standardized_tokens:
            if token.get("chain") in ["solana", "sol"]:
                solana_tokens.append(token)

        logging.info(f"Found {len(solana_tokens)} Solana-based tokens.")

        # Analyze each token and collect results.
        for token in solana_tokens:
            token["upside_score"] = analyze_token(token)
            token["rug_score"], analyzed_risks = fetch_rugcheck_score(
                self.enviroment["RUGCHECK_API_URL"], token.get("address", None)
            )

        # Sort results by the upside score in descending order.
        # results.sort(key=lambda x: x["upside_score"], reverse=True)
        logger.info(
            f"Found {len(solana_tokens)} tokens with a potential upside score. which are: {solana_tokens}"
        )

        return solana_tokens

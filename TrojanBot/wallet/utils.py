import os
import base58
import logging
import requests

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def base58_to_32byte(base58_string):
    """
    Converts a Base58 encoded string to a 32-byte representation.

    Args:
        base58_string: The Base58 encoded string.

    Returns:
        A 32-byte string, or None if the input is invalid.
    """
    try:
        decoded = base58.b58decode(base58_string)
        if len(decoded) != 32:
            logger.warn("Decoded base58 string not up to 32")
            return None
        return decoded
    except ValueError:
        logger.error("Value error in base58 decoding")
        return None


def get_token_price(symbol, currency: str = "usd"):
    coingeko_url = os.getenv("COINGEKO_URL")
    url = f"{coingeko_url}/simple/price?ids={symbol}&vs_currencies={currency}"
    response = requests.get(url)
    return response.json().get(symbol, {}).get(currency, 0)

def calc_balance(price, amount):
    return price * amount

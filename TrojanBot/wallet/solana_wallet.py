import os
import logging
import requests

from datetime import datetime
from solders.pubkey import Pubkey
from solana.rpc.api import Client

# from .utils import base58_to_32byte

logger = logging.getLogger(__name__)
network_status = os.getenv("NETWORK_STATUS")

# Validate a Solana wallet address
def is_valid_solana_address(address):
    try:
        Pubkey(address)
        return True
    except Exception as e:
        logger.warning(f"Invalid wallet address: {address} - {e}")
        return False


# Fetch balance of a Solana wallet address
def get_solana_balance(address):
    client = Client(os.getenv(f"SOLANA_CLIENT_{network_status}"))
    try:
        resp = client.get_balance(Pubkey(address))
        lamports = resp.value  
        return round(lamports / 1e9, 5)
    except Exception as e:
        logger.error(f"Error fetching balance: {e}")
        return None


# Swap using Jupiter Aggregator API (Simulated tx - client must sign)
def get_jupiter_swap(from_token, to_token, amount, user_public_key):
    try:
        url = os.getenv(f"SWAP_API_{network_status}")
        payload = {
            "inputMint": from_token,
            "outputMint": to_token,
            "amount": amount,
            "userPublicKey": user_public_key,
            "slippageBps": 50,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        logger.error(f"Jupiter swap error: {e}")
        return None


# if __name__ == "__main__":
#     test_address = "525JvScCLgpmPoMgWJB6C8CpyDPt43LPBqLVZa6j4MLw"

#     if is_valid_solana_address(base58_to_32byte(test_address)):
#         balance = get_solana_balance(base58_to_32byte(test_address))
#         print(f"Wallet {test_address} balance: {balance} SOL")
#     else:
#         print("Invalid wallet address")

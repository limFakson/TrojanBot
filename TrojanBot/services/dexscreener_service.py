import requests
import logging

logger = logging.getLogger(__name__)

# request headers
headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}

def fetch_token_pair_details(url, chainId, tokenAddress):
    url = f"{url}/token-pairs/v1/{chainId}/{tokenAddress}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        for d in data:
            base_token = d.get("baseToken")
            return {
                "name": base_token["name"],
                "symbol": base_token["symbol"],
                "priceUsd": d.get("priceUsd", ""),
                "volume": d.get("volume"),
                "liquidity": d.get("liquidity"),
                "marketCap": d.get("marketCap"),
                "priceChange": d.get("priceChange"),
            }
    except Exception as e:
        logging.error(f"Error fetching token pairs: {e}")
        return {}


def fetch_dexscreener_tokens(url):
    """
    Fetch token data from dexscreener.com.
    (Update the URL and response parsing as needed based on the actual API.)
    """
    url = f"{url}/token-profiles/latest/v1"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Assume that token pairs are listed under a key called "pairs"
        for token in data:
            token["source"] = "dexscreener"
            logging.info(f"Fetching {token['tokenAddress']} details.")
            pairsAddress = fetch_token_pair_details(
                url, token["chainId"], token["tokenAddress"]
            )
            token.update(pairsAddress)

        logging.info(f"Fetched {len(data)} tokens from dexscreener.")
        return data
    except Exception as e:
        logging.error(f"Error fetching dexscreener tokens: {e}")
        return []

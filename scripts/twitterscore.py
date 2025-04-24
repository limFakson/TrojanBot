import requests
import logging
import time
import os

# Set up basic logging.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Retrieve your TwitterScore API key from an environment variable (or replace with your key).
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "your_api_key_here")

def fetch_pump_fun_tokens():
    """
    Fetch token data from pump.fun.
    Adjust the URL and parsing according to the actual API.
    """
    url = "https://pump.fun/api/tokens"  # Example endpoint; update as needed.
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Assume tokens are under the "data" key.
        tokens = data.get("data", [])
        # Tag each token with its source.
        for token in tokens:
            token["source"] = "pump.fun"
        logging.info(f"Fetched {len(tokens)} tokens from pump.fun.")
        return tokens
    except Exception as e:
        logging.error(f"Error fetching pump.fun tokens: {e}")
        return []

def fetch_dexscreener_tokens():
    """
    Fetch token data from dexscreener.com.
    Adjust the URL and JSON parsing as needed.
    """
    url = "https://api.dexscreener.com/latest/dex/tokens"  # Example endpoint; update as needed.
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Assume tokens (or trading pairs) are under a key called "pairs".
        tokens = data.get("pairs", [])
        for token in tokens:
            token["source"] = "dexscreener"
        logging.info(f"Fetched {len(tokens)} tokens from dexscreener.")
        return tokens
    except Exception as e:
        logging.error(f"Error fetching dexscreener tokens: {e}")
        return []

def standardize_token(token, source):
    """
    Standardize token data from either source into a common format.
    Note: We assume that one or both sources provide a 'twitter' field.
    """
    if source == "pump.fun":
        return {
            "name": token.get("name", "Unknown"),
            "symbol": token.get("symbol", "N/A"),
            "chain": token.get("chain", "").lower(),  # e.g. "solana"
            "volume": float(token.get("volume", 0)),
            "price_change": float(token.get("priceChange", 0)),
            "liquidity": float(token.get("liquidity", 0)),
            "twitter": token.get("twitter", None)  # Assuming pump.fun provides this
        }
    elif source == "dexscreener":
        return {
            "name": token.get("pairName", "Unknown"),
            "symbol": token.get("baseTokenSymbol", "N/A"),
            "chain": token.get("chain", "").lower(),  # e.g. "solana"
            "volume": float(token.get("volume", 0)),
            "price_change": float(token.get("priceChange", 0)),
            "liquidity": float(token.get("liquidity", 0)),
            "twitter": token.get("twitter", None)  # Adjust as needed
        }
    else:
        return {}

def extract_features(token):
    """
    Extract features for analysis (e.g., volume, price change, liquidity).
    """
    volume = token.get("volume", 0)
    price_change = token.get("price_change", 0)
    liquidity = token.get("liquidity", 0)
    return [volume, price_change, liquidity]

def dummy_ai_score(features):
    """
    Dummy “AI” scoring function that computes an upside score.
    Replace this with your actual machine learning model.
    """
    volume, price_change, liquidity = features
    score = (price_change * 0.6) + (volume * 0.3) + (liquidity * 0.1)
    return score

def analyze_token(token):
    """
    Analyze token features to produce an upside score.
    """
    features = extract_features(token)
    score = dummy_ai_score(features)
    return score

def fetch_twitter_info(twitter_handle, api_key=TWITTER_API_KEY):
    """
    Query the TwitterScore API to retrieve information about the given Twitter (X) handle.
    Expected returned fields: overall_score, top_followers, and trust_level.
    
    Adjust the URL, header, and JSON key names based on the actual API documentation.
    """
    url = f"https://api.twitterscore.io/score?handle={twitter_handle}"
    headers = {}
    if api_key and api_key != "your_api_key_here":
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Adjust keys below as per the actual API response.
        twitter_data = {
            "overall_score": data.get("overall_score", None),
            "top_followers": data.get("top_followers", []),
            "trust_level": data.get("trust_level", None)
        }
        logging.info(f"Fetched Twitter info for handle: {twitter_handle}")
        return twitter_data
    except Exception as e:
        logging.error(f"Error fetching Twitter info for {twitter_handle}: {e}")
        return {}

def main():
    # Fetch tokens from pump.fun and dexscreener.com.
    pump_tokens = fetch_pump_fun_tokens()
    dexscreener_tokens = fetch_dexscreener_tokens()

    # Combine and standardize tokens.
    all_tokens_raw = pump_tokens + dexscreener_tokens
    standardized_tokens = []
    for token in all_tokens_raw:
        source = token.get("source", "")
        std_token = standardize_token(token, source)
        standardized_tokens.append(std_token)

    # Filter for Solana-based tokens.
    solana_tokens = [
        token for token in standardized_tokens
        if token.get("chain", "") in ["solana", "sol"]
    ]
    logging.info(f"Found {len(solana_tokens)} Solana-based tokens.")

    # Analyze each token and enrich with Twitter info.
    results = []
    for token in solana_tokens:
        # Calculate an upside score using the dummy AI function.
        score = analyze_token(token)
        twitter_info = {}
        twitter_handle = token.get("twitter")
        if twitter_handle:
            twitter_info = fetch_twitter_info(twitter_handle)
        results.append({
            "name": token.get("name"),
            "symbol": token.get("symbol"),
            "upside_score": score,
            "twitter_handle": twitter_handle,
            "twitter_info": twitter_info
        })

    # Sort the results by upside score (highest first).
    results.sort(key=lambda x: x["upside_score"], reverse=True)

    # Display the results.
    print("\n--- Solana Token Analysis ---")
    for r in results:
        print(f"{r['name']} ({r['symbol']}): Upside Score = {r['upside_score']:.2f}")
        if r["twitter_handle"]:
            twitter_data = r.get("twitter_info", {})
            overall = twitter_data.get("overall_score", "N/A")
            trust = twitter_data.get("trust_level", "N/A")
            top_followers = twitter_data.get("top_followers", [])
            print(f"   Twitter Handle: {r['twitter_handle']}")
            print(f"   Overall Twitter Score: {overall}")
            print(f"   Trust Level: {trust}")
            print(f"   Top Followers: {top_followers}")
        else:
            print("   No Twitter handle available.")
        print("-------------------------")

if __name__ == "__main__":
    main()

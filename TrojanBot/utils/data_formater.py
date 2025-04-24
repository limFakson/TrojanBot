
def extract_features(token):
    """
    Extract numeric features from the standardized token data.
    This includes trading volume, recent price change, and liquidity.
    """
    try:
        volume = token.get("volume", {})
        price_change = token.get("price_change", {})
        liquidity = token.get("liquidity", {})
        print(volume)
        print(liquidity)
        print(price_change)
        # Extract specific values with defaults to 0 if missing
        vol_24h = volume.get("h24", 0)  # 24-hour volume
        price_change_1h = price_change.get("h1", 0)  # Price change in 1 hour
        liquidity_usd = liquidity.get("usd", 0)  # Liquidity in USD

        return [vol_24h, price_change_1h, liquidity_usd]
    except Exception as e:
        print(f"Failes to fetch features: {e}")


def dummy_ai_score(features):
    """
    A simple scoring function that returns an upside score.
    Uses a weighted sum of the extracted features.
    """
    volume, price_change, liquidity = features

    # Arbitrary weight factors; adjust based on model logic
    score = (price_change * 0.6) + (volume * 0.3) + (liquidity * 0.1)

    return round(score, 2)


def analyze_token(token):
    """
    Analyze a token’s features to produce a profitability/upside score.
    Replace the dummy_ai_score with your actual ML model prediction as needed.
    """
    features = extract_features(token)
    score = dummy_ai_score(features)
    return score


def standardize_token(token, source):
    """
    Convert token data from a given source into a standardized format.
    Adjust the keys based on the actual response structure.
    """
    if source == "pump.fun":
        # Example mapping – update the keys as needed.
        return {
            "name": token.get("name", "Unknown"),
            "symbol": token.get("symbol", "N/A"),
            "chain": token.get("chain", "").lower(),  # e.g., "solana" expected
            "volume": float(token.get("volume", 0)),
            "price_change": float(token.get("priceChange", 0)),
            "liquidity": float(token.get("liquidity", 0)),
        }
    elif source == "dexscreener":
        # Example mapping – update the keys as needed.
        return {
            "name": token.get("name", "Unknown"),
            "symbol": token.get("symbol", "N/A"),
            "chain": token.get("chainId", "").lower(),  # e.g., "solana" expected
            "volume": token.get("volume", {}),
            "price_change": token.get("priceChange", {}),
            "liquidity": token.get("liquidity", {}),
        }
    else:
        return {}

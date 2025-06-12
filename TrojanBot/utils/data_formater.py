import base58

def extract_features(token):
    """
    Extract numeric features from the standardized token data.
    This includes trading volume, recent price change, and liquidity.
    """
    try:
        volume = token.get("volume", {})
        price_change = token.get("price_change", {})
        liquidity = token.get("liquidity")

        # Extract specific values with defaults to 0 if missing
        vol_24h = volume.get("h24", 0)  # 24-hour volume
        price_change_1h = price_change.get("h1", 0)  # Price change in 1 hour
        if "usd" in liquidity:
            liquidity_usd = liquidity.get("usd")
        else:
            liquidity_usd = 0
        
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
            return None
        return decoded
    except ValueError:
        return None

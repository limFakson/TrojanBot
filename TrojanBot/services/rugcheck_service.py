import requests
import logging

logger = logging.getLogger(__name__)


# ============================
# RUGCHECK INTEGRATION
# ============================
def fetch_rugcheck_score(url, address):
    """
    Query the RugCheck API to retrieve the contract safety score.
    Adjust the URL and JSON keys based on the actual API.
    """
    url = f"{url}/tokens/{address}/report"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rug_score = data.get("score", None)
        analyzed_risk = analyze_risk(data.get("risks", []))
        return rug_score, analyzed_risk
    except Exception as e:
        logging.error(f"Error fetching RugCheck score for {address}: {e}")
        return None

def analyze_risk(risks:list):
    """
    Analyze the risk score and return a message.
    """
    coin_risks = {}
    for risk in risks:
        coin_risks[risk['name']] = {
            'score': risk['score'],
            'description': risk['description'],
            'level': risk['level'],
        }
    

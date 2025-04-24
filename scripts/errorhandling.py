import joblib
model = joblib.load('your_trained_model.pkl')

def analyze_token(token):
    features = extract_features(token)
    score = model.predict([features])[0]
    return score

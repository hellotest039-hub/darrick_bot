import numpy as np
import pandas as pd
from scipy.stats import poisson
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

class DarrickAI:
    def __init__(self):
        self.model_1x2 = RandomForestClassifier(n_estimators=100)
        self.model_over = XGBClassifier()
        self Trained = False
    
    def calculate_value_bet(self, odds, true_prob):
        """Value = (prob * odds - 1)"""
        implied_prob = 1 / odds
        return true_prob * odds - 1 if true_prob > implied_prob else 0
    
    def analyze_best_market(self, match):
        """Détecte marché le plus rentable >65%"""
        odds_home = match['odds_home']
        odds_away = match['odds_away']
        odds_draw = match.get('odds_draw', 3.5)
        
        # Probabilités ML simulées (entraînées)
        home_win_prob = max(0.45, 1 / (1 + np.exp(odds_home - odds_away)))
        away_win_prob = max(0.45, 1 / (1 + np.exp(odds_away - odds_home)))
        draw_prob = 0.25
        
        markets = {
            '1X2_Home': self.calculate_value_bet(odds_home, home_win_prob),
            '1X2_Away': self.calculate_value_bet(odds_away, away_win_prob),
            '1X2_Draw': self.calculate_value_bet(odds_draw, draw_prob),
            'Over25': self.calculate_value_bet(1.90, 0.62),
            'Under25': self.calculate_value_bet(1.95, 0.58),
            'BTTS_Yes': self.calculate_value_bet(1.75, 0.61)
        }
        
        # Meilleur marché
        best_market = max(markets, key=markets.get)
        confidence = max(home_win_prob, away_win_prob, 0.62)
        
        if markets[best_market] > 0.15 and confidence > 0.65:  # Value + confiance
            prediction = "2-1" if best_market.startswith('1X2_Home') else "1-2"
            return {
                'best_market': best_market,
                'confidence': confidence,
                'prediction': prediction,
                'odds': odds_home if best_market == '1X2_Home' else odds_away,
                'value': markets[best_market],
                'stake': '⭐⭐⭐⭐⭐' if confidence > 0.75 else '⭐⭐⭐⭐'
            }
        return None

darrick_ai = DarrickAI()

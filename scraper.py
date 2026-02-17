import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
from datetime import datetime

class DarrickScraper:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        ]
        self.session = requests.Session()
    
    def get_live_odds(self):
        """Scraping OddsPortal + données de test"""
        headers = {'User-Agent': random.choice(self.user_agents)}
        
        # Données réelles simulées (OddsPortal structure)
        live_matches = [
            {'home': 'PSG', 'away': 'Lyon', 'odds_home': 1.72, 'odds_draw': 3.80, 'odds_away': 4.50},
            {'home': 'Man Utd', 'away': 'Liverpool', 'odds_home': 2.45, 'odds_draw': 3.40, 'odds_away': 2.80},
            {'home': 'Bayern', 'away': 'Dortmund', 'odds_home': 1.65, 'odds_draw': 4.00, 'odds_away': 5.25},
            {'home': 'Real Madrid', 'away': 'Barca', 'odds_home': 2.10, 'odds_draw': 3.60, 'odds_away': 3.20},
            {'home': 'Juventus', 'away': 'Inter', 'odds_home': 2.30, 'odds_draw': 3.30, 'odds_away': 3.00}
        ]
        
        return pd.DataFrame(live_matches)

scraper = DarrickScraper()

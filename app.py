import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import time
import re

# AUTH
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🤖 **DARRICK BOT PRO v5.0**")
    col1, col2 = st.columns(2)
    with col1: username = st.text_input("👤", placeholder="darrick_bot")
    with col2: password = st.text_input("🔑", type="password")
    
    if st.button("🚀 LIVE", type="primary"):
        if username == "darrick_bot" and password == "P3tanqu3#.":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌")
    st.stop()

st.markdown("# 🤖 **DARRICK BOT - MATCHS RÉELS 1xBet/FIFA**")

# === SCRAPING 1XBET RÉEL ===
@st.cache_data(ttl=30)
def scrape_1xbet_real():
    """Scraping VRAI 1xBet live (multi-régions)"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
        'Referer': 'https://1xbet.ci/'
    }
    
    # URLs 1xBet AFRICA (accessibles)
    urls = [
        "https://1xbet.ci/fr/line/football",  # Pré-match
        "https://1xbet.bj/fr/line/football",  # Bénin
        "https://1xbetwh.com/fr/line/football" # Afrique
    ]
    
    all_matches = []
    
    for url in urls:
        try:
            print(f"Scraping {url}...")
            resp = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            # 1xBet selectors réels
            events = soup.select('.c-events__item, .event-item, [data-event]')
            for event in events[:15]:  # Top 15
                try:
                    teams = event.select('.event__participant, .team-name, .c-events__team')
                    if len(teams) >= 2:
                        home = teams[0].get_text(strip=True)[:25]
                        away = teams[1].get_text(strip=True)[:25]
                        
                        # Score/odds
                        score_elem = event.select_one('.score, .live-score, .odds')
                        score = score_elem.get_text(strip=True) if score_elem else "Pré-match"
                        
                        all_matches.append({
                            'home': home,
                            'away': away,
                            'score': score,
                            'time': datetime.now().strftime('%H:%M'),
                            'source': url.split('/')[-1],
                            'type': '1xBet RÉEL'
                        })
                except:
                    continue
                    
            time.sleep(2)  # Anti-ban
        except Exception as e:
            st.error(f"Erreur {url}: {e}")
            continue
    
    return pd.DataFrame(all_matches)

# === FIFA eSPORTS RÉEL ===
@st.cache_data(ttl=60)
def scrape_fifa_esports():
    """FIFA eSports + Virtual Football réel"""
    headers = {'User-Agent': 'Mozilla/5.0 (Android 12)'}
    
    # Sites eSports FIFA accessibles
    urls = [
        "https://www.flashscore.fr/esports/fifa/",
        "https://www.oddsportal.com/esports/fifa/",
        "https://www.sofascore.com/esports/fifa"
    ]
    
    fifa_matches = []
    
    for url in urls:
        try:
            resp = requests.get(url, headers=headers, timeout=12)
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            # FIFA events
            games = soup.select('.event__match, .esport-match, .game-row')[:10]
            for game in games:
                try:
                    home = game.select_one('.home-team, .event__participant--home')
                    away = game.select_one('.away-team, .event__participant--away')
                    
                    if home and away:
                        fifa_matches.append({
                            'home': home.get_text(strip=True)[:25],
                            'away': away.get_text(strip=True)[:25],
                            'score': 'LIVE' if 'live' in game.get('class', []) else 'Pré-match',
                            'time': 'En cours',
                            'source': 'eSports',
                            'type': 'FIFA eSports'
                        })
                except:
                    continue
        except:
            continue
    
    return pd.DataFrame(fifa_matches)

# === INTERFACE ===
tab1, tab2, tab3 = st.tabs(["🔴 1xBet RÉEL", "🎮 FIFA/eSports", "📊 MIXTE"])

with tab1:
    st.subheader("🔴 **1xBet Football LIVE**")
    with st.spinner("🔍 Scraping 1xBet..."):
        real_matches = scrape_1xbet_real()
    
    if not real_matches.empty:
        for _, match in real_matches.head(12).iterrows():
            col1, col2, col3 = st.columns([3, 3, 3])
            with col1: st.markdown(f"**🏠 {match['home']}**")
            with col2: st.markdown(f"**✈️ {match['away']}**")
            with col3: st.info(f"📊 {match['score']} | {match['source']}")
    else:
        st.warning("⚠️ Aucun match 1xBet trouvé (essayez plus tard)")

with tab2:
    st.subheader("🎮 **FIFA eSports LIVE**")
    with st.spinner("🔍 Scraping FIFA..."):
        fifa_matches = scrape_fifa_esports()
    
    if not fifa_matches.empty:
        for _, match in fifa_matches.iterrows():
            col1, col2 = st.columns([4, 3])
            with col1: st.markdown(f"**🎮 {match['home']} vs {match['away']}**")
            with col2: st.success(f"**{match['score']}** | {match['source']}")
    else:
        st.info("⏳ FIFA eSports chargement...")

with tab3:
    st.subheader("🔥 **TOUS MATCHS**")
    all_matches = pd.concat([scrape_1xbet_real(), scrape_fifa_esports()], ignore_index=True)
    if not all_matches.empty:
        st.dataframe(all_matches[['home', 'away', 'score', 'type', 'source']])
    else:
        st.info("📡 Recherche matchs en cours...")

# MÉTRIQUES
col1, col2, col3 = st.columns(3)
col1.metric("🎯 Prédictions", len(scrape_1xbet_real()))
col2.metric("⚽ 1xBet", "Scraping LIVE")
col3.metric("🎮 FIFA", "eSports OK")

st.markdown("*🤖 Darrick Bot v5.0 | Scraping 1xBet/FIFA RÉEL | Render Live*")
        

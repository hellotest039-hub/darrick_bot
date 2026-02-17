import sqlite3
import pandas as pd
from datetime import datetime

def init_database():
    conn = sqlite3.connect('darrick.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        home_team TEXT,
        away_team TEXT,
        match_date TEXT,
        best_market TEXT,
        confidence REAL,
        prediction TEXT,
        real_result TEXT,
        odds REAL,
        accuracy INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        market_type TEXT,
        total_predictions INTEGER,
        success_rate REAL,
        roi REAL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

def save_prediction(home, away, market, confidence, prediction, odds):
    conn = sqlite3.connect('darrick.db')
    cursor = conn.execute('''INSERT INTO predictions 
                           (home_team, away_team, best_market, confidence, prediction, odds)
                           VALUES (?, ?, ?, ?, ?, ?)''',
                         (home, away, market, confidence, prediction, odds))
    pred_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pred_id

def update_result(pred_id, real_result):
    conn = sqlite3.connect('darrick.db')
    cursor = conn.execute("SELECT prediction, best_market FROM predictions WHERE id=?", (pred_id,))
    pred_data = cursor.fetchone()
    
    if pred_data:
        prediction = pred_data[0]
        market = pred_data[1]
        accuracy = 1 if real_result == prediction else 0
        
        conn.execute("""UPDATE predictions SET real_result=?, accuracy=?, updated_at=CURRENT_TIMESTAMP 
                       WHERE id=?""", (real_result, accuracy, pred_id))
        conn.commit()
    
    conn.close()

def get_stats():
    conn = sqlite3.connect('darrick.db')
    df = pd.read_sql_query("""
        SELECT best_market, AVG(confidence) as avg_confidence, 
               AVG(accuracy) as accuracy, COUNT(*) as total 
        FROM predictions 
        WHERE accuracy IS NOT NULL 
        GROUP BY best_market 
        ORDER BY accuracy DESC
    """, conn)
    conn.close()
    return df

init_database()

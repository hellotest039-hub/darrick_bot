import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

def get_darrick_stats():
    """Statistiques complètes Darrick Bot"""
    conn = sqlite3.connect('darrick.db')
    
    # Stats par marché
    market_stats = pd.read_sql_query("""
        SELECT best_market, 
               COUNT(*) as total_predictions,
               AVG(confidence) as avg_confidence,
               AVG(accuracy) as accuracy_rate,
               AVG(odds) as avg_odds
        FROM predictions 
        WHERE accuracy IS NOT NULL
        GROUP BY best_market
        ORDER BY accuracy_rate DESC
    """, conn)
    
    # Stats globales
    global_stats = pd.read_sql_query("""
        SELECT 
            COUNT(*) as total_predictions,
            AVG(accuracy) as global_accuracy,
            AVG(confidence) as avg_confidence,
            SUM(CASE WHEN accuracy = 1 THEN 1 ELSE 0 END) as wins,
            COUNT(*) - SUM(CASE WHEN accuracy = 1 THEN 1 ELSE 0 END) as losses
        FROM predictions 
        WHERE accuracy IS NOT NULL
    """, conn)
    
    conn.close()
    return market_stats, global_stats

def display_stats_dashboard():
    """Dashboard stats PRO"""
    market_stats, global_stats = get_darrick_stats()
    
    if not market_stats.empty:
        # Graphique performance marchés
        fig = px.bar(market_stats.head(5), 
                    x='best_market', y='accuracy_rate',
                    title="🏆 Performance par Marché",
                    color='accuracy_rate',
                    color_continuous_scale='RdYlGn',
                    text='accuracy_rate')
        fig.update_traces(texttemplate='%{text:.1%}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Métriques globales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎯 Accuracy Globale", 
                     f"{global_stats['global_accuracy'].iloc[0]:.1%}")
        with col2:
            st.metric("📊 Prédictions", 
                     f"{global_stats['total_predictions'].iloc[0]}")
        with col3:
            win_rate = global_stats['wins'].iloc[0] / global_stats['total_predictions'].iloc[0]
            st.metric("✅ Taux Victoire", f"{win_rate:.1%}")
        with col4:
            st.metric("⭐ Confiance Moyenne", 
                     f"{global_stats['avg_confidence'].iloc[0]:.1%}")
        
        st.dataframe(market_stats)

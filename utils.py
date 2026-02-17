import streamlit as st
import plotly.express as px
import pandas as pd

def display_prediction_card(prediction, match):
    """Carte prédiction PRO"""
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        st.markdown(f"**🏠 {match['home']}**")
    with col2:
        st.markdown(f"**✈️ {match['away']}**")
    with col3:
        st.info(f"💰 {match['odds_home']:.2f} | {match['odds_away']:.2f}")
        
        st.success(f"""
        🎯 **{prediction['best_market']}**
        **{prediction['confidence']:.0%}** 
        (@{prediction['odds']:.2f})
        💎 Value: +{prediction['value']:.2f}
        {prediction['stake']}
        """)

def show_performance_chart(stats_df):
    """Graphique performance"""
    if not stats_df.empty:
        fig = px.bar(stats_df, x='best_market', y='accuracy',
                    title="Performance par Marché",
                    color='accuracy', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, height=400)

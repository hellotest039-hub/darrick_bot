import streamlit as st
import hashlib

USERNAME = "darrick_bot"
PASSWORD_HASH = hashlib.sha256("P3tanqu3#.".encode()).hexdigest()

def check_credentials(username, password):
    return (username == USERNAME and 
            hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH)

def login_interface():
    st.markdown("""
    <style>
    .login-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        max-width: 450px;
        margin: 2rem auto;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    }
    .logo { font-size: 3.5em; margin-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='login-container'>
        <div class='logo'>🤖</div>
        <h1>DARRICK BOT PRO</h1>
        <p>IA Prédictions Football Professionnelle</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    with col2:
        username = st.text_input("👤 Nom d'utilisateur", placeholder="darrick_bot")
        password = st.text_input("🔑 Mot de passe", type="password", placeholder="••••••••")
        
        if st.button("🚀 ACCÉDER AU BOT", type="primary", use_container_width=True):
            if check_credentials(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Connexion réussie, Darrick !")
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects")
    
    return 'logged_in' in st.session_state and st.session_state.logged_in

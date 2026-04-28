import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus", layout="wide", initial_sidebar_state="collapsed")

# --- CSS POUR REPRODUIRE L'IMAGE EXACTEMENT ---
st.markdown("""
    <style>
    /* Global */
    .stApp {
        background-color: #5d0909; /* Fond bordeaux comme l'image */
        background: linear-gradient(180deg, #3d0000 0%, #1a0000 100%);
        color: white;
    }
    
    /* Header/Navbar */
    .nav {
        display: flex;
        justify-content: space-between;
        padding: 15px 5%;
        background: rgba(0,0,0,0.5);
        position: fixed; top: 0; width: 100%; z-index: 99;
    }

    /* Hero Section */
    .hero {
        padding: 120px 10% 60px 10%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .hero-text { flex: 1; }
    .hero-title { font-size: 50px; font-weight: bold; line-height: 1.1; }
    .red-btn {
        background-color: #ff0000;
        color: white;
        padding: 12px 30px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 20px;
    }

    /* Cards Section */
    .section-title { text-align: center; font-size: 35px; margin: 50px 0; }
    .card-container {
        display: flex;
        justify-content: space-around;
        gap: 20px;
        padding: 0 5%;
    }
    .card {
        background: white;
        color: black;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        flex: 1;
        border-bottom: 5px solid #ff0000;
    }
    .card h3 { color: #ff0000; }

    /* Footer Contact */
    .footer {
        background: #000;
        padding: 50px 10%;
        margin-top: 100px;
        display: flex;
        justify-content: space-between;
    }
    
    /* Cacher les éléments Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stButton>button {
        background-color: #ff0000 !important;
        color: white !important;
        border: none !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION STATE ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"

def go_to(name):
    st.session_state.page = name
    st.rerun()

# ==========================================
# HEADER (SITE WEB)
# ==========================================
st.markdown("""
    <div class="nav">
        <div style="font-weight:bold; font-size:22px;">PATIENT<span style="color:red;">PLUS</span></div>
        <div style="display:flex; gap:20px; font-size:14px; padding-top:5px;">
            ACCUEIL &nbsp;&nbsp; SERVICES &nbsp;&nbsp; STATISTIQUES &nbsp;&nbsp; CONTACT
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# CONTENU DE L'ACCUEIL (COMME SUR L'IMAGE)
# ==========================================
if st.session_state.page == "Accueil":
    
    # --- HERO SECTION ---
    st.markdown("""
        <div class="hero">
            <div class="hero-text">
                <p style="color:red; font-weight:bold; letter-spacing:2px;">NOTRE MISSION</p>
                <h1 class="hero-title">Votre avis améliore <br> la santé au <span style="color:red;">Cameroun</span></h1>
                <p style="max-width:500px; margin-top:20px; opacity:0.8;">
                    Patient Plus est une plateforme d'audit citoyen. 
                    Ensemble, mesurons la qualité de service de nos hôpitaux pour garantir 
                    des soins d'excellence et une sécurité totale.
                </p>
            </div>
            <div style="flex:1; text-align:right;">
                <img src="https://cdn-icons-png.flaticon.com/512/2750/2750657.png" width="300">
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- SERVICES SECTION (LES 3 CARTES) ---
    st.markdown("<h2 class='section-title'>Nos services hospitaliers</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="card"><h3>Hôpitaux Généraux</h3><p>Référence (HGY, HGD). Oncologie, Dialyse et Chirurgie complexe.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="card"><h3>Hôpitaux Centraux</h3><p>HCY, Laquintinie. Centres névralgiques pour les urgences traumatiques.</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="card"><h3>Gynéco-Obstétrique</h3><p>Spécialisé Mère-Enfant (Yaoundé/Douala). Priorité à la santé néonatale.</p></div>""", unsafe_allow_html=True)
    
    # --- STATISTIQUES SECTION ---
    st.markdown("<h2 class='section-title'>Statistiques de performance</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div style="padding:20px; background:rgba(255,255,255,0.1); border-radius:10px;">
                <h4 style="color:red;">Efficience : 48%</h4>
                <p>Seul 48% des hôpitaux publics atteignent les objectifs de performance. Votre audit aide à corriger cela.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div style="padding:20px; background:rgba(255,255,255,0.1); border-radius:10px;">
                <h4 style="color:red;">Mortalité Maternelle</h4>
                <p>Défi majeur : 550 décès pour 100k naissances. Nous priorisons l'audit des maternités.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- BOUTON POUR PASSER AU FORMULAIRE ---
    st.markdown("<br><br><center>", unsafe_allow_html=True)
    if st.button("CRÉER MON COMPTE & RÉPONDRE AU FORMULAIRE"):
        go_to("Connexion")
    st.markdown("</center>", unsafe_allow_html=True)

    # --- FOOTER / CONTACT ---
    st.markdown("""
        <div class="footer">
            <div>
                <h3>CONTACTEZ-NOUS</h3>
                <p>📍 Yaoundé, Cameroun</p>
                <p>📞 +237 600 000 000</p>
            </div>
            <div style="width:400px;">
                <p>Laissez un message à l'équipe Patient Plus</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE DE CONNEXION / CRÉATION COMPTE
# ==========================================
elif st.session_state.page == "Connexion":
    st.markdown("<br><br><br><center><h1>Accès sécurisé</h1></center>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("auth"):
            st.text_input("Nom d'utilisateur / Email")
            st.text_input("Mot de passe", type="password")
            if st.form_submit_button("S'INSCRIRE ET CONTINUER"):
                go_to("Formulaire")

# ==========================================
# PAGE DU FORMULAIRE DYNAMIQUE
# ==========================================
elif st.session_state.page == "Formulaire":
    st.markdown("<br><br><br><h2>Formulaire d'audit patient</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.subheader("1. Identification")
        st.text_input("Nom")
        st.text_input("Prénom")
        
        # --- DATE DE NAISSANCE JUSQU'A 1915 ---
        st.date_input("Date de naissance", 
                      min_value=datetime(1915, 1, 1), 
                      value=datetime(1990, 1, 1))
        
        st.text_input("Email ou Numéro de téléphone")
        
        st.subheader("2. Détails de la visite")
        hopital = st.selectbox("Hôpital consulté", ["HGY Yaoundé", "HGD Douala", "HCY Yaoundé", "Laquintinie", "HGOPY"])
        service = st.selectbox("Service visité", ["Urgences", "Imagerie", "Laboratoire", "Chirurgie", "Pharmacie"])
        
        st.subheader("3. Évaluation du service")
        # Questions adaptées
        if service == "Urgences":
            st.radio("Délai entre arrivée et triage respecté ?", ["Oui", "Non", "Partiellement"])
            st.radio("Protocole urgences vitales affiché ?", ["Oui", "Non"])
        elif service == "Chirurgie":
            st.radio("Check-list sécurité OMS remplie ?", ["Oui", "Non"])
            st.radio("Vérification règle des '5 B' faite ?", ["Oui", "Non"])
        
        st.subheader("4. Expérience Patient")
        st.select_slider("Le personnel s'est-il identifié ?", ["Pas du tout", "Moyen", "Parfaitement"])
        st.select_slider("Respect de votre dignité et intimité ?", ["Médiocre", "Bien", "Excellent"])
        
        if st.button("SOUMETTRE MON AUDIT"):
            st.success("Merci ! Vos données sont transmises en toute confidentialité.")
            if st.button("Retour à l'accueil"): go_to("Accueil")

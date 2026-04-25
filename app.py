import streamlit as st
import pandas as pd
import sqlite3

# --- 1. CONFIGURATION (TOUJOURS EN PREMIER) ---
st.set_page_config(page_title="Patient Plus", layout="wide", initial_sidebar_state="collapsed")

# --- 2. INITIALISATION DU SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"

def changer_page(nom):
    st.session_state.page = nom

# --- 3. DESIGN CSS (REPRODUCTION EXACTE IMAGE) ---
st.markdown("""
    <style>
    /* Fond sombre */
    .stApp {
        background-color: #001e46;
        color: white;
    }

    /* Conteneur pour les boutons invisibles de Streamlit */
    .stButton button {
        width: 100%;
        height: 220px;
        background-color: transparent !important;
        color: transparent !important;
        border: none !important;
        position: absolute;
        z-index: 10;
        cursor: pointer;
    }

    /* Les Bulles (Cards) comme sur l'image */
    .nav-card {
        background-color: #122a45; /* Bleu marine de l'image */
        border: 2px solid white;    /* Bordure blanche fine */
        border-radius: 15px;       /* Coins arrondis */
        padding: 30px 10px;
        text-align: center;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: 0.3s;
    }

    .nav-card:hover {
        background-color: #1c3d63;
        transform: scale(1.02);
    }

    .card-icon { font-size: 45px; margin-bottom: 10px; }
    .card-title { font-size: 26px; font-weight: bold; color: white; text-transform: uppercase; letter-spacing: 1px; }
    .card-subtitle { font-size: 15px; color: #cbd5e0; margin-top: 5px; }
    
    /* Titre de section */
    .nav-header {
        text-align: center;
        font-weight: bold;
        letter-spacing: 2px;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        padding-bottom: 10px;
        margin: 40px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIQUE DES PAGES ---

if st.session_state.page == "Accueil":
    # Titre principal
    st.markdown("<h1 style='text-align:center; font-size:60px; margin-bottom:0;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px; opacity:0.8;'>Amélioration du traitement de service dans les services d'urgence</p>", unsafe_allow_html=True)

    st.markdown("<div class='nav-header'>NAVIGUER DANS L'APPLICATION</div>", unsafe_allow_html=True)

    # Création des 3 bulles
    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("clic_audit", key="btn_audit", on_click=lambda: changer_page("Audit"))
        st.markdown("""
            <div class="nav-card">
                <div class="card-icon">📝</div>
                <div class="card-title">AUDIT</div>
                <div class="card-subtitle">Participer à l'enquête</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.button("clic_admin", key="btn_admin", on_click=lambda: changer_page("Admin"))
        st.markdown("""
            <div class="nav-card">
                <div class="card-icon">🔐</div>
                <div class="card-title">ADMIN</div>
                <div class="card-subtitle">Espace Enquêteur</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.button("clic_infos", key="btn_infos", on_click=lambda: changer_page("Infos"))
        st.markdown("""
            <div class="nav-card">
                <div class="card-icon">ℹ️</div>
                <div class="card-title">INFOS</div>
                <div class="card-subtitle">À propos du projet</div>
            </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == "Audit":
    st.title("📝 Formulaire d'Audit")
    if st.button("Retour à l'accueil"):
        changer_page("Accueil")
    st.info("Le formulaire d'enquête s'affiche ici.")

# (Ajoute tes sections Admin et Infos ici de la même manière)

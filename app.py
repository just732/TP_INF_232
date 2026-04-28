import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="MediCollect Cameroon", layout="centered", initial_sidebar_state="collapsed")

# --- INITIALISATION DU STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "HOME"

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('medicollect.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urgences 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, heure TEXT, motif TEXT, 
                  gravite TEXT, lit_dispo BOOLEAN, patient_id TEXT, statut TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- CSS PERSONNALISÉ (STYLE EXACT DES IMAGES) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fond général */
    .stApp {
        background-color: #FFFFFF;
    }

    /* --- HEADER --- */
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0px;
        border-bottom: 1px solid #EEEEEE;
        margin-bottom: 20px;
    }
    .header-title {
        color: #003399;
        font-weight: 700;
        font-size: 20px;
        display: flex;
        align-items: center;
    }

    /* --- CARTES DE COLLECTION (PAGE FORMS) --- */
    .form-card {
        background: white;
        border: 1px solid #E0E0E0;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        position: relative;
    }
    .priority-tag {
        position: absolute;
        top: 20px;
        right: 20px;
        background: #E8F0FE;
        color: #1967D2;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .card-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
    }

    /* --- BOUTONS PRINCIPAUX --- */
    .stButton>button {
        background-color: #004085 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100% !important;
        padding: 12px !important;
        font-weight: 600 !important;
    }

    /* --- NAVIGATION BAS DE PAGE --- */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        display: flex;
        justify-content: space-around;
        padding: 15px 0;
        border-top: 1px solid #EEEEEE;
        z-index: 1000;
    }
    .nav-item {
        text-align: center;
        color: #999999;
        font-size: 12px;
        text-decoration: none;
    }
    .nav-item.active {
        color: #003399;
    }

    /* --- STATUS SYNC BOX --- */
    .sync-box {
        background-color: #E8F0FE;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }
    
    /* --- FORMULAIRE GRAVITÉ --- */
    .severity-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 10px 0;
    }
    .severity-btn {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        cursor: pointer;
    }
    
    /* Cacher les éléments Streamlit inutiles */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- COMPOSANT HEADER ---
st.markdown(f"""
    <div class="header">
        <div class="header-title">
            <span style="margin-right:10px;">✚</span> MediCollect Cameroon
        </div>
        <div style="font-size:24px;">👤</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE : ACCUEIL (Image 3)
# ==========================================
if st.session_state.page == "HOME":
    # Image de fond style hero (utilise l'image de l'hôpital que tu as fournie)
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg", use_column_width=True)
    
    st.markdown("""
        <div style="text-align:center; padding: 20px 0;">
            <h1 style="font-size: 28px; color: #1a1a1a;">Améliorons ensemble nos urgences</h1>
            <p style="color: #666;">Collectez des données précises pour transformer les soins de santé au Cameroun.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Commencer la collecte →"):
        navigate_to("FORMS")
        
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div style="background:#F0F4F8; padding:20px; border-radius:15px; text-align:center;"><h2 style="margin:0; color:#004085;">12k+</h2><p style="margin:0; font-size:12px;">RAPPORTS</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="background:#F0F4F8; padding:20px; border-radius:15px; text-align:center;"><h2 style="margin:0; color:#004085;">45</h2><p style="margin:0; font-size:12px;">HÔPITAUX</p></div>', unsafe_allow_html=True)

# ==========================================
# PAGE : DATA COLLECTION (Image 2)
# ==========================================
elif st.session_state.page == "FORMS":
    st.markdown("<h3>Data Collection</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#666;'>Select an operational form to begin recording healthcare metrics.</p>", unsafe_allow_html=True)
    
    # Carte 1 : Admission Urgences
    with st.container():
        st.markdown("""
            <div class="form-card">
                <div class="priority-tag">High Priority</div>
                <div class="card-icon" style="background:#FFEBEB; color:#FF4D4D;">✱</div>
                <div style="font-weight:700; font-size:18px;">Admission Urgences</div>
                <p style="font-size:14px; color:#666;">Record critical patient intake details for emergency room admissions.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Entry →", key="btn_urg"):
            navigate_to("URGENCE_FORM")

    # Carte 2 : Disponibilité Personnel
    st.markdown("""
        <div class="form-card">
            <div class="card-icon" style="background:#E6FFFA; color:#38B2AC;">👥</div>
            <div style="font-weight:700; font-size:18px;">Disponibilité du Personnel</div>
            <p style="font-size:14px; color:#666;">Daily staff attendance and shifts tracking for departmental coverage.</p>
            <div style="color:#004085; font-weight:600; font-size:14px; cursor:pointer;">Update Roster →</div>
        </div>
    """, unsafe_allow_html=True)

    # Status Sync
    st.markdown("""
        <div class="sync-box">
            <div style="font-size:12px; font-weight:700; color:#1967D2; letter-spacing:1px;">SYSTEM HEALTH</div>
            <div style="font-size:20px; font-weight:700; margin-bottom:10px;">Sync Status: Online</div>
            <p style="font-size:14px; color:#555;">All forms submitted are being synchronized with the Ministry of Public Health database in real-time.</p>
            <div style="color:#2D9748; font-size:14px;">● Regional Cloud Connected</div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE : FORMULAIRE URGENCE (Image 4 & 5)
# ==========================================
elif st.session_state.page == "URGENCE_FORM":
    st.markdown("<p style='color:#004085; font-weight:700; font-size:12px;'>✱ URGENT CARE INTAKE</p>", unsafe_allow_html=True)
    st.markdown("<h2>Admission Urgences</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#666;'>Formulaire de saisie rapide pour le tri des patients.</p>", unsafe_allow_html=True)
    
    # Barre de progression
    st.markdown('<div style="width:100%; height:6px; background:#E0E0E0; border-radius:10px;"><div style="width:33%; height:100%; background:#004085; border-radius:10px;"></div></div><br>', unsafe_allow_html=True)

    with st.container():
        heure = st.text_input("Heure d'arrivée", value="02:30 PM")
        motif = st.text_area("Motif de consultation", placeholder="Décrivez brièvement les symptômes...")
        
        st.markdown("<b>Niveau de gravité</b>", unsafe_allow_html=True)
        gravite = st.radio("", ["Faible", "Moyen", "Urgent", "Critique"], horizontal=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        lit = st.toggle("Lit disponible ? / Confirmer l'espace en salle de tri")
        
        if st.button("Soumettre les données"):
            # Logique SQL
            conn = sqlite3.connect('medicollect.db')
            c = conn.cursor()
            p_id = f"CMR-{datetime.now().strftime('%S%M')}-04-12"
            c.execute("INSERT INTO urgences (heure, motif, gravite, lit_dispo, patient_id, statut) VALUES (?,?,?,?,?,?)",
                      (heure, motif, gravite, lit, p_id, "Vérifié"))
            conn.commit()
            conn.close()
            st.success("Données enregistrées !")

    # Footer du formulaire
    st.markdown(f"""
        <div style="background:#F0F4F8; padding:15px; border-radius:12px; margin-top:20px; display:flex; align-items:center;">
            <div style="font-size:24px; margin-right:15px;">👤</div>
            <div>
                <div style="font-size:12px; color:#666;">Patient ID</div>
                <div style="font-weight:700;">CMR-992-04-12</div>
            </div>
        </div>
        <div style="background:#F0F4F8; padding:15px; border-radius:12px; margin-top:10px; display:flex; align-items:center;">
            <div style="font-size:24px; margin-right:15px; color:#2D9748;">🛡️</div>
            <div>
                <div style="font-size:12px; color:#666;">Statut</div>
                <div style="color:#2D9748; font-weight:700;">Vérifié</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Retour"):
        navigate_to("FORMS")

# ==========================================
# BARRE DE NAVIGATION FIXE (Bas de l'écran)
# ==========================================
st.markdown(f"""
    <div class="nav-bar">
        <a href="javascript:void(0)" class="nav-item {'active' if st.session_state.page == 'HOME' else ''}">
            <div style="font-size:20px;">🏠</div>
            HOME
        </a>
        <a href="javascript:void(0)" class="nav-item {'active' if st.session_state.page in ['FORMS', 'URGENCE_FORM'] else ''}">
            <div style="font-size:20px;">📋</div>
            FORMS
        </a>
        <a href="javascript:void(0)" class="nav-item">
            <div style="font-size:20px;">📊</div>
            DASHBOARD
        </a>
    </div>
""", unsafe_allow_html=True)

# Ajout d'espace pour que la nav bar ne cache pas le contenu
st.markdown("<br><br><br>", unsafe_allow_html=True)

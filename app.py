import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'admin_auth' not in st.session_state: st.session_state.admin_auth = False

def changer_page(nom): st.session_state.page = nom

# --- DONNÉES ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU", "Gynéco-Obstétrique"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie", "Hôpital de Bonassama"],
    "Extrême-Nord": ["Hôpital Régional de Maroua", "Hôpital de Kousseri"],
    "Nord": ["Hôpital Régional de Garoua"], "Est": ["Hôpital Régional de Bertoua"],
    "Ouest": ["Hôpital Régional de Bafoussam"], "Sud": ["Hôpital Régional d'Ebolowa"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda"], "Sud-Ouest": ["Hôpital Régional de Buea"]
}

# --- DESIGN CSS (BULLES ULTRA-LARGES ET MÉLANGE BLANC/BLEU) ---
st.markdown("""
    <style>
    /* Fond global : Hôpital Général de Yaoundé */
    .stApp {
        background: linear-gradient(rgba(0, 20, 50, 0.8), rgba(0, 20, 50, 0.8)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* TITRES */
    .title-main { text-align: center; font-size: 80px; font-weight: 900; color: white; margin-bottom: 0px; }
    .subtitle-main { text-align: center; font-size: 22px; color: white; margin-bottom: 40px; opacity: 0.9; }
    .nav-header { text-align: center; font-size: 28px; font-weight: bold; color: white; margin-bottom: 30px; text-transform: uppercase; }

    /* LES BULLES GÉANTES (MÉLANGE BLEU MARINE ET BLANC) */
    div.nav-container .stButton > button {
        height: 320px !important; /* Plus haute */
        width: 100% !important;   /* Plus large */
        /* MÉLANGE DE COULEURS : Dégradé du Bleu Marine vers le Blanc/Gris clair */
        background: linear-gradient(135deg, #1a3352 0%, #1a3352 50%, #ffffff 100%) !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 25px !important;
        font-size: 26px !important;
        font-weight: bold !important;
        white-space: pre-wrap !important;
        transition: 0.4s !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Changement de couleur du texte sur la partie blanche au survol */
    div.nav-container .stButton > button:hover {
        transform: translateY(-15px) scale(1.02) !important;
        background: linear-gradient(135deg, #ffffff 0%, #1a3352 50%, #1a3352 100%) !important;
        color: #1a3352 !important;
        border-color: #e1395f !important;
    }

    /* PETIT BOUTON RETOUR RECTANGULAIRE */
    .back-btn .stButton > button {
        height: 35px !important; 
        width: 120px !important; 
        font-size: 13px !important;
        background-color: rgba(255, 255, 255, 0.2) !important; 
        border: 1px solid white !important;
        border-radius: 5px !important;
        color: white !important;
    }

    /* Boites d'infos stats */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 20px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 10px solid #e1395f;
    }
    label { color: white !important; font-weight: bold; }
    .white-box { background: white; padding: 40px; border-radius: 20px; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('patient_plus_final_national.db', check_same_thread=False)
def init_db():
    conn = get_connection(); c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, email TEXT, region TEXT, hopital TEXT, 
                    motif TEXT, attente INTEGER, eval_inf TEXT, eval_med TEXT, 
                    suggestions TEXT, date_soumission DATETIME)''')
    conn.commit(); conn.close()
init_db()

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<div class='title-main'>PATIENT PLUS</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-main'>Système National d'Amélioration du Traitement dans les Services d'Urgence</div>", unsafe_allow_html=True)

    # Dashboard automatique
    conn = get_connection(); df = pd.read_sql_query("SELECT * FROM rapports", conn); conn.close()
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Audits", len(df)), c2.metric("Attente Moy.", f"{round(df['attente'].mean(),1)}m"), c3.metric("Régions", df['region'].nunique())

    col_a, col_b = st.columns(2)
    with col_a: st.markdown('<div class="info-card"><h4>Performance</h4><p>Analyse des 172 établissements publics camerounais.</p></div>', unsafe_allow_html=True)
    with col_b: st.markdown('<div class="info-card"><h4>Maternité</h4><p>Sécurisation des 35,9% de naissances hors milieu médical.</p></div>', unsafe_allow_html=True)

    st.markdown("<div class='nav-header'>NAVIGUER DANS L'APPLICATION</div>", unsafe_allow_html=True)

    # --- LES TROIS BULLES ULTRA-LARGES DÉGRADÉES ---
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        st.button("📝 AUDIT\n\nParticiper à l'enquête", on_click=lambda: changer_page("Audit"))
    with n2:
        st.button("🔐 ADMIN\n\nEspace Enquêteur", on_click=lambda: changer_page("Admin"))
    with n3:
        st.button("ℹ️ INFOS\n\nÀ propos du projet", on_click=lambda: changer_page("Infos"))
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2 : AUDIT ---
elif st.session_state.page == "Audit":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    with st.form("audit_f"):
        st.subheader("Identification")
        nom, prenom, email = st.text_input("Nom"), st.text_input("Prénom"), st.text_input("Email")
        reg = st.selectbox("Région", list(data_cameroun.keys()))
        hop = st.selectbox("Hôpital", data_cameroun[reg])
        attente = st.slider("Attente (min)", 0, 300, 30)
        e_inf = st.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
        e_med = st.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
        sug = st.text_area("Suggestions")
        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = get_connection(); c = conn.cursor()
            c.execute("INSERT INTO rapports (nom, prenom, email, region, hopital, attente, eval_inf, eval_med, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                     (nom, prenom, email, reg, hop, attente, e_inf, e_med, sug, datetime.now()))
            conn.commit(); conn.close()
            st.success("Transmis."); changer_page("Accueil")

# --- PAGE 3 : ADMIN ---
elif st.session_state.page == "Admin":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    pwd = st.text_input("Code", type="password")
    if st.button("ACCÉDER"):
        if pwd == "admin123":
            conn = get_connection(); df = pd.read_sql_query("SELECT * FROM rapports", conn); conn.close()
            st.markdown("<div class='white-box'>", unsafe_allow_html=True)
            st.dataframe(df)
            st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 4 : INFOS ---
elif st.session_state.page == "Infos":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div class='white-box'><h3>À propos</h3><p>Patient Plus est la plateforme d'audit citoyen pour le Cameroun.</p></div>", unsafe_allow_html=True)

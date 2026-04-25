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
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU de Yaoundé", "Hôpital Gynéco-Obstétrique"],
    "Est": ["Hôpital Régional de Bertoua", "Hôpital de District de Batouri"],
    "Extrême-Nord": ["Hôpital Régional de Maroua", "Hôpital de District de Mokolo"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie", "Hôpital de District de Bonassama"],
    "Nord": ["Hôpital Régional de Garoua", "Hôpital de District de Guider"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda", "Hôpital de District de Wum"],
    "Ouest": ["Hôpital Régional de Bafoussam", "Hôpital de District de Dschang"],
    "Sud": ["Hôpital Régional d'Ebolowa", "Hôpital de District de Kribi"],
    "Sud-Ouest": ["Hôpital Régional de Buea", "Hôpital Régional de Limbe"]
}

# --- DESIGN CSS (REPRODUCTION EXACTE DE LA 2ÈME IMAGE) ---
st.markdown("""
    <style>
    /* Image de fond Hôpital Général */
    .stApp {
        background: linear-gradient(rgba(0, 20, 50, 0.85), rgba(0, 20, 50, 0.85)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* SECTION NAVIGUER DANS L'APPLICATION */
    .nav-header {
        text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;
    }

    /* REPRODUCTION DES BULLES (CARTES HORIZONTALES) */
    div.nav-card-container > div > div > button {
        height: 220px !important; /* Format rectangulaire horizontal */
        width: 100% !important;
        background-color: #1a3352 !important; /* Bleu marine identique à l'image */
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important; /* Bordure blanche fine */
        border-radius: 15px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        white-space: pre-wrap !important; /* Permet le retour à la ligne pour le sous-titre */
        transition: 0.3s !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1.5 !important;
    }

    /* Effet au survol (changement de couleur subtil) */
    div.nav-card-container > div > div > button:hover {
        background-color: #24446d !important;
        border-color: white !important;
        transform: translateY(-5px) !important;
    }

    /* PETIT BOUTON RETOUR RECTANGULAIRE (SOBRE) */
    .back-btn-box .stButton > button {
        height: 35px !important; width: 110px !important; font-size: 13px !important;
        background-color: rgba(255, 255, 255, 0.1) !important; border: 1px solid white !important;
        border-radius: 4px !important; color: white !important;
    }

    /* Info cards stats */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 15px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 8px solid #e1395f;
    }
    label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('audit_v16_final.db', check_same_thread=False)
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, email TEXT, region TEXT, hopital TEXT, 
                    motif TEXT, attente INTEGER, eval_inf TEXT, justif_inf TEXT, 
                    eval_med TEXT, justif_med TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()
init_db()

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:70px; font-weight:900;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:22px; margin-bottom:40px;'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>", unsafe_allow_html=True)

    # Dashboard de synthèse (KPIs) automatique
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("AUDITS COMPLÉTÉS", len(df))
        c2.metric("ATTENTE MOYENNE", f"{round(df['attente'].mean(), 1)} MIN")
        c3.metric("RÉGIONS AUDITÉES", df['region'].nunique())

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="info-card"><h4>Infrastructure Publique</h4><p>Analyse des 172 hôpitaux publics du Cameroun pour optimiser la performance nationale.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="info-card"><h4>Services Maternité</h4><p>Analyse des 35,9% de naissances hors milieu assisté pour renforcer la sécurité sanitaire.</p></div>', unsafe_allow_html=True)

    # --- SECTION NAVIGATION PAR BULLES (REPRODUCTION EXACTE) ---
    st.markdown("<div class='nav-header'>NAVIGUER DANS L'APPLICATION</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="nav-card-container">', unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        st.button("📝 AUDIT\n\nParticiper à l'enquête", on_click=lambda: changer_page("Audit"))
    with n2:
        st.button("🔐 ADMIN\n\nEspace Enquêteur", on_click=lambda: changer_page("Admin"))
    with n3:
        st.button("ℹ️ INFOS\n\nÀ propos du projet", on_click=lambda: changer_page("Infos"))
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2 : AUDIT PATIENT ---
elif st.session_state.page == "Audit":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.header("Formulaire d'Audit National")
    with st.form("audit_form"):
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        email, age = c1.text_input("Email"), c2.number_input("Âge", 0, 110, 25)
        reg = st.selectbox("Sélectionnez votre Région", list(data_cameroun.keys()))
        hop = st.selectbox("Établissement visité", data_cameroun[reg])
        motif = st.text_area("Raison de votre présence à l'hôpital")
        attente = st.slider("Temps d'attente estimé (min)", 0, 300, 30)
        
        ci, cm = st.columns(2)
        e_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
        j_inf = ci.text_area("Justification (Infirmières)")
        e_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
        j_med = cm.text_area("Justification (Médecins)")
        sug = st.text_area("Vos recommandations pour améliorer cet hôpital")

        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO rapports (nom, prenom, age, email, region, hopital, motif, attente, eval_inf, justif_inf, eval_med, justif_med, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                     (nom, prenom, age, email, reg, hop, motif, attente, e_inf, j_inf, e_med, j_med, sug, datetime.now()))
            conn.commit()
            conn.close()
            st.success("Données envoyées avec succès.")
            changer_page("Accueil")

# --- PAGE 3 : ADMIN ---
elif st.session_state.page == "Admin":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)

    pwd = st.text_input("Veuillez entrer le code de sécurité enquêteur", type="password")
    if st.button("DÉVERROUILLER LES DONNÉES"):
        if pwd == "admin123":
            conn = get_connection()
            df = pd.read_sql_query("SELECT * FROM rapports", conn)
            conn.close()
            st.write("### Rapports d'audit collectés")
            st.dataframe(df)
        else: st.error("Code de sécurité incorrect.")

# --- PAGE 4 : INFOS ---
elif st.session_state.page == "Infos":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='background:white; padding:30px; border-radius:15px; color:black;'><h3>À propos</h3><p>Patient Plus est un outil de collecte de données pour l'audit du système hospitalier camerounais.</p></div>", unsafe_allow_html=True)

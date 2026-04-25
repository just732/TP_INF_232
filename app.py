import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION DE LA NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'admin_auth' not in st.session_state: st.session_state.admin_auth = False
if 'investigateur' not in st.session_state: st.session_state.investigateur = None

def changer_page(nom): st.session_state.page = nom

# --- DONNÉES NATIONALES (10 RÉGIONS) ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU de Yaoundé", "Hôpital Gynéco-Obstétrique"],
    "Est": ["Hôpital Régional de Bertoua", "Hôpital de District de Abong-Mbang"],
    "Extrême-Nord": ["Hôpital Régional de Maroua", "Hôpital de District de Kousseri"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie", "Hôpital de District de Bonassama"],
    "Nord": ["Hôpital Régional de Garoua", "Hôpital de District de Guider"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda", "Hôpital de District de Wum"],
    "Ouest": ["Hôpital Régional de Bafoussam", "Hôpital de District de Dschang"],
    "Sud": ["Hôpital Régional d'Ebolowa", "Hôpital de District de Kribi"],
    "Sud-Ouest": ["Hôpital Régional de Buea", "Hôpital Régional de Limbe"]
}

# --- DESIGN CSS (REPRODUCTION EXACTE DE VOTRE IMAGE) ---
st.markdown("""
    <style>
    /* Image de fond : Hôpital Général de Yaoundé */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.85), rgba(0, 43, 92, 0.85)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* DESIGN DES BULLES (CARTES BLEUES DE L'IMAGE) */
    .nav-bubble .stButton > button {
        height: 250px !important;
        width: 100% !important;
        background-color: #1a3352 !important; /* Bleu marine exact */
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important; /* Bordure blanche fine */
        border-radius: 15px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        white-space: pre-wrap !important;
        transition: 0.4s !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4) !important;
    }
    
    .nav-bubble .stButton > button:hover {
        background-color: #24446d !important;
        transform: translateY(-10px) !important;
        border-color: white !important;
    }

    /* PETIT BOUTON RETOUR RECTANGULAIRE */
    .back-container .stButton > button {
        height: 35px !important;
        width: 110px !important;
        font-size: 13px !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        border: 1px solid white !important;
        margin-bottom: 20px !important;
    }

    /* Cartes d'information statistiques */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 15px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 8px solid #e1395f;
    }
    .white-box { background-color: white; padding: 30px; border-radius: 15px; color: #1a1a1a; }
    label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('patient_plus_vfinal.db', check_same_thread=False)
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
    st.markdown("<h1 style='text-align:center; font-size:70px; margin-bottom:0;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:22px; padding:0 50px;'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>", unsafe_allow_html=True)

    # Dashboard de synthèse automatique
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("AUDITS COMPLÉTÉS", len(df))
        c2.metric("ATTENTE MOYENNE", f"{round(df['attente'].mean(), 1)} min")
        c3.metric("RÉGIONS COUVERTES", df['region'].nunique())

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="info-card"><h4>Performance Hospitalière</h4><p>Analyse des 172 hôpitaux publics du Cameroun pour optimiser la qualité des soins.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="info-card"><h4>Santé Maternelle</h4><p>35,9% des naissances hors milieu médical. Vos données aident à réformer ces services.</p></div>', unsafe_allow_html=True)

    # --- NAVIGATION PAR BULLES (DESIGN EXACT IMAGE 2) ---
    st.markdown("<br><h3 style='text-align:center;'>NAVIGUER DANS L'APPLICATION</h3><br>", unsafe_allow_html=True)
    
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown('<div class="nav-bubble">', unsafe_allow_html=True)
        st.button("📝 AUDIT\n\nParticiper à l'enquête", on_click=lambda: changer_page("Audit"))
        st.markdown('</div>', unsafe_allow_html=True)
    with n2:
        st.markdown('<div class="nav-bubble">', unsafe_allow_html=True)
        st.button("🔐 ADMIN\n\nEspace Enquêteur", on_click=lambda: changer_page("Admin"))
        st.markdown('</div>', unsafe_allow_html=True)
    with n3:
        st.markdown('<div class="nav-bubble">', unsafe_allow_html=True)
        st.button("ℹ️ INFOS\n\nÀ propos du projet", on_click=lambda: changer_page("Infos"))
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2 : AUDIT PATIENT ---
elif st.session_state.page == "Audit":
    st.markdown('<div class="back-container">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.header("Formulaire d'Audit National Cameroun")
    with st.form("audit_form"):
        c1, c2 = st.columns(2)
        nom, prenom, email = c1.text_input("Nom"), c2.text_input("Prénom"), c1.text_input("Email")
        age, reg = c2.number_input("Âge", 0, 110, 25), st.selectbox("Sélectionnez la Région", list(data_cameroun.keys()))
        hop = st.selectbox("Établissement visité", data_cameroun[reg])
        motif, attente = st.text_area("Raison de votre consultation"), st.slider("Délai d'attente urgences (min)", 0, 300, 30)
        
        ci, cm = st.columns(2)
        e_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
        j_inf = ci.text_area("Justification (Personnel Infirmier)")
        e_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
        j_med = cm.text_area("Justification (Corps Médical)")
        sug = st.text_area("Vos recommandations concrètes d'amélioration")

        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO rapports (nom, prenom, age, email, region, hopital, motif, attente, eval_inf, justif_inf, eval_med, justif_med, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                     (nom, prenom, age, email, reg, hop, motif, attente, e_inf, j_inf, e_med, j_med, sug, datetime.now()))
            conn.commit()
            conn.close()
            st.success("Données transmises avec succès. Merci !")
            changer_page("Accueil")

# --- PAGE 3 : ESPACE ADMIN ---
elif st.session_state.page == "Admin":
    st.markdown('<div class="back-container">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)

    t1, t2 = st.tabs(["👤 Identification", "📊 Rapports d'Audit"])
    with t1:
        st.markdown("<div class='white-box'>", unsafe_allow_html=True)
        with st.form("admin_c"):
            nom_e = st.text_input("Nom de l'enquêteur")
            if st.form_submit_button("CRÉER MON COMPTE"):
                st.session_state.investigateur = nom_e
                st.success(f"Compte enquêteur actif : {nom_e}")
        st.markdown("</div>", unsafe_allow_html=True)
    with t2:
        pwd = st.text_input("Code de sécurité", type="password")
        if pwd == "admin123":
            conn = get_connection()
            df = pd.read_sql_query("SELECT * FROM rapports", conn)
            conn.close()
            st.write(df)

# --- PAGE 4 : INFOS ---
elif st.session_state.page == "Infos":
    st.markdown('<div class="back-container">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div class='white-box'><h3>À propos du projet</h3><p>Patient Plus est une solution d'audit quantitatif dédiée à la réforme hospitalière nationale au Cameroun.</p></div>", unsafe_allow_html=True)

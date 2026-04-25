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
if 'investigateur' not in st.session_state: st.session_state.investigateur = None

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

# --- DESIGN CSS (REPRODUCTION EXACTE DE VOTRE IMAGE) ---
st.markdown("""
    <style>
    /* Image de fond Hôpital Général de Yaoundé */
    .stApp {
        background: linear-gradient(rgba(0, 20, 50, 0.8), rgba(0, 20, 50, 0.8)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* REPRODUCTION DES BULLES (CARTES BLEUES) */
    .stButton > button {
        height: 250px !important; 
        width: 100% !important;
        background-color: #1a3352 !important; /* Bleu marine exact de l'image */
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important; /* Bordure blanche fine */
        border-radius: 15px !important;
        transition: 0.3s !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        white-space: pre-wrap !important;
        font-size: 20px !important;
    }

    /* Effet au survol */
    .stButton > button:hover {
        border-color: white !important;
        background-color: #24446d !important;
        transform: translateY(-8px) !important;
    }

    /* PETIT BOUTON RETOUR RECTANGULAIRE (DISCRET) */
    .back-btn-box .stButton > button {
        height: 35px !important;
        width: 110px !important;
        font-size: 13px !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 4px !important;
        border: 1px solid white !important;
        margin-bottom: 20px !important;
    }

    /* Info cards pour les statistiques */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 15px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 8px solid #e1395f;
    }
    label { color: white !important; font-weight: bold; }
    .white-box { background-color: white; padding: 30px; border-radius: 20px; color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('patient_plus_final_v1.db', check_same_thread=False)
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, sexe TEXT, metier TEXT, dob TEXT, 
                    region TEXT, domicile TEXT, email TEXT, maladie TEXT, service TEXT, 
                    hopital TEXT, attente INTEGER, eval_inf TEXT, justif_inf TEXT, 
                    eval_med TEXT, justif_med TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()
init_db()

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:70px;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:22px;'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>", unsafe_allow_html=True)

    # Statistiques Dynamiques (Analyse descriptive)
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        st.markdown("### 📊 État de l'Audit National")
        c1, c2, c3 = st.columns(3)
        c1.metric("AUDITS RÉALISÉS", len(df))
        c2.metric("ATTENTE MOYENNE", f"{round(df['attente'].mean(), 1)} min")
        c3.metric("RÉGIONS COUVERTES", df['region'].nunique())

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="info-card"><h4>Hôpitaux Publics</h4><p>Le Cameroun compte 172 hôpitaux. Cet audit vise à accroître la performance globale estimée à 48%.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="info-card"><h4>Maternité</h4><p>35,9% des naissances hors milieu médical. Vos réponses aident à sécuriser ces services.</p></div>', unsafe_allow_html=True)

    # --- NAVIGATION PAR BULLES (STYLE EXACT DE L'IMAGE 2) ---
    st.markdown("<br><h3 style='text-align:center;'>NAVIGUER DANS L'APPLICATION</h3><br>", unsafe_allow_html=True)
    
    n1, n2, n3 = st.columns(3)
    with n1:
        st.button("📝 AUDIT\n\nParticiper à l'enquête", on_click=lambda: changer_page("Audit"))
    with n2:
        st.button("🔐 ADMIN\n\nEspace Enquêteur", on_click=lambda: changer_page("Admin"))
    with n3:
        st.button("ℹ️ INFOS\n\nÀ propos du projet", on_click=lambda: changer_page("Infos"))

# --- PAGE 2 : AUDIT ---
elif st.session_state.page == "Audit":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.header("Formulaire d'Audit National")
    with st.form("audit_form"):
        st.subheader("1. Identification")
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        age, sexe = c1.number_input("Âge", 0, 110, 25), c2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier, dob = c1.text_input("Métier"), c2.date_input("Date de naissance")
        email, dom = c1.text_input("Email"), c2.text_input("Lieu de résidence")
        
        st.subheader("2. Contexte Médical")
        reg = st.selectbox("Région", list(data_cameroun.keys()))
        hop = st.selectbox("Hôpital", data_cameroun[reg])
        service, maladie = st.text_input("Service visité"), st.text_input("Motif/Maladie")
        
        st.subheader("3. Évaluation")
        attente = st.slider("Attente (min)", 0, 300, 30)
        ci, cm = st.columns(2)
        e_inf, j_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"]), ci.text_area("Justification (Infirmières)")
        e_med, j_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"]), cm.text_area("Justification (Médecins)")
        
        st.subheader("4. Recommandations")
        sug = st.text_area("Suggestions d'amélioration")
        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, region, domicile, email, maladie, service, hopital, attente, eval_inf, justif_inf, eval_med, justif_med, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                     (nom, prenom, age, sexe, metier, str(dob), reg, dom, email, maladie, service, hop, attente, e_inf, j_inf, e_med, j_med, sug, datetime.now()))
            conn.commit()
            conn.close()
            st.success("Audit envoyé.")
            changer_page("Accueil")

# --- PAGE 3 : ADMIN ---
elif st.session_state.page == "Admin":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)

    tab_c, tab_r = st.tabs(["👤 Créer Compte", "📊 Résultats"])
    with tab_c:
        st.markdown("<div class='white-box'>", unsafe_allow_html=True)
        with st.form("admin_c"):
            nom_e = st.text_input("Nom Enquêteur")
            email_e = st.text_input("Email")
            if st.form_submit_button("VALIDER"):
                st.session_state.investigateur = nom_e
                st.success("Compte créé.")
        st.markdown("</div>", unsafe_allow_html=True)
    with tab_r:
        pwd = st.text_input("Code", type="password")
        if pwd == "admin123":
            conn = get_connection()
            df = pd.read_sql_query("SELECT * FROM rapports", conn)
            conn.close()
            st.write(df)

# --- PAGE 4 : INFOS ---
elif st.session_state.page == "Infos":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div class='white-box'><h3>Infos Projet</h3><p>Audit citoyen pour la santé nationale au Cameroun.</p></div>", unsafe_allow_html=True)

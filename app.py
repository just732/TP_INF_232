import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION DE LA NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"

def changer_page(nom_page):
    st.session_state.page = nom_page

# --- DONNÉES NATIONALES ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU de Yaoundé", "Hôpital Gynéco-Obstétrique"],
    "Est": ["Hôpital Régional de Bertoua", "Hôpital de District de Batouri"],
    "Extrême-Nord": ["Hôpital Régional de Maroua", "Hôpital de District de Kousseri"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie", "Hôpital de District de Bonassama"],
    "Nord": ["Hôpital Régional de Garoua", "Hôpital de District de Guider"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda", "Hôpital de District de Wum"],
    "Ouest": ["Hôpital Régional de Bafoussam", "Hôpital de District de Dschang"],
    "Sud": ["Hôpital Régional d'Ebolowa", "Hôpital de District de Kribi"],
    "Sud-Ouest": ["Hôpital Régional de Buea", "Hôpital Régional de Limbe"]
}

# --- DESIGN CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    /* Image de fond : Hôpital Général */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.8), rgba(0, 43, 92, 0.8)), 
                    url('https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* Bulles d'Information (Images de fond) */
    .info-bubble {
        background-size: cover; padding: 25px; border-radius: 25px; color: #1a1a1a; 
        margin-bottom: 20px; border-left: 10px solid #e1395f; min-height: 280px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .img-pediatrie { background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url('https://www.social-sante.gouv.fr/IMG/jpg/pediatrie_hopital.jpg'); }
    .img-maternite { background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url('https://www.unicef.org/cameroon/sites/unicef.org.cameroon/files/styles/hero_desktop/public/UNI354546.jpg'); }

    /* Bulles Flottantes de Navigation (Cartes) */
    .nav-card {
        background-color: rgba(255, 255, 255, 0.15);
        border: 2px solid white; border-radius: 20px; padding: 30px; text-align: center;
        transition: 0.3s; cursor: pointer; height: 100%;
    }
    .nav-card:hover { background-color: #e1395f; transform: translateY(-10px); }
    
    /* Boutons invisibles par-dessus les cartes */
    .stButton>button {
        background-color: #e1395f !important; color: white !important;
        border-radius: 50px !important; width: 100%; font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_national_v7.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, sexe TEXT, metier TEXT, dob TEXT, 
                    region TEXT, domicile TEXT, email TEXT,
                    maladie TEXT, service TEXT, hopital TEXT, attente INTEGER, 
                    eval_inf TEXT, justif_inf TEXT, eval_med TEXT, justif_med TEXT,
                    rdv_ligne TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- LOGIQUE DES PAGES ---

# 1. PAGE D'ACCUEIL
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:60px;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:24px;'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>", unsafe_allow_html=True)

    # Bulles d'informations Cameroon
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown("""<div class="info-bubble img-pediatrie">
            <h4>📊 Performance Hospitalière</h4>
            <p><b>Hôpitaux Régionaux :</b> 4 000 à 6 000 hospitalisations/an. Surcharge critique.</p>
            <p><b>Statut :</b> Seuls 48% des 172 hôpitaux publics sont jugés performants au Cameroun.</p>
        </div>""", unsafe_allow_html=True)
    with col_info2:
        st.markdown("""<div class="info-bubble img-maternite">
            <h4>👶 Maternité et Nouveau-nés</h4>
            <p><b>Accouchements :</b> 35,9% se font encore à domicile sans assistance médicale.</p>
            <p>L'audit aide à identifier les freins à l'admission institutionnelle.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align:center;'>QUE SOUHAITEZ-VOUS FAIRE ?</h2>", unsafe_allow_html=True)
    
    # BULLES FLOTTANTES DE NAVIGATION
    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        st.markdown('<div class="nav-card"><h3>📝 AUDIT</h3><p>Remplir le formulaire de satisfaction patient.</p></div>', unsafe_allow_html=True)
        st.button("OUVRIR LE FORMULAIRE", on_click=lambda: changer_page("Formulaire"))
    with nav2:
        st.markdown('<div class="nav-card"><h3>📊 ANALYSE</h3><p>Consulter les statistiques en temps réel.</p></div>', unsafe_allow_html=True)
        st.button("VOIR LES RÉSULTATS", on_click=lambda: changer_page("Admin"))
    with nav3:
        st.markdown('<div class="nav-card"><h3>ℹ️ INFOS</h3><p>En savoir plus sur le projet Patient Plus.</p></div>', unsafe_allow_html=True)
        st.button("À PROPOS", on_click=lambda: changer_page("Infos"))

# 2. PAGE FORMULAIRE
elif st.session_state.page == "Formulaire":
    st.button("⬅ RETOUR À L'ACCUEIL", on_click=lambda: changer_page("Accueil"))
    st.markdown("<h2>📝 Formulaire d'Audit National</h2>", unsafe_allow_html=True)
    
    with st.form("audit_form"):
        st.subheader("1. Identification")
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        age, sexe = c1.number_input("Âge", 0, 110, 25), c2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier, email = c1.text_input("Métier"), c2.text_input("Email")
        dob = c1.date_input("Date de naissance")
        
        st.subheader("2. Localisation")
        reg = st.selectbox("Région du Cameroun :", list(data_cameroun.keys()))
        hop = st.selectbox("Hôpital fréquenté :", data_cameroun[reg])
        dom = st.text_input("Quartier de résidence")

        st.subheader("3. Évaluation")
        maladie, serv = st.text_input("Maladie/Motif"), st.text_input("Service visité")
        attente = st.slider("Attente aux urgences (min)", 0, 300, 30)
        
        ci, cm = st.columns(2)
        e_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
        j_inf = ci.text_area("Justification Infirmières")
        e_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
        j_med = cm.text_area("Justification Médecins")

        st.subheader("4. Suggestions")
        sug = st.text_area("Comment améliorer le service ?")
        rdv = st.radio("Prendre RDV en ligne avec un médecin spécifique ?", ["Oui", "Non"])

        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = get_connection()
            c = conn.cursor()
            c.execute('''INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, region, domicile, email,
                        maladie, service, hopital, attente, eval_inf, justif_inf, eval_med, justif_med,
                        rdv_ligne, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                     (nom, prenom, age, sexe, metier, str(dob), reg, dom, email, maladie, serv, hop, attente, e_inf, j_inf, e_med, j_med, rdv, sug, datetime.now()))
            conn.commit()
            conn.close()
            st.success("✅ Audit envoyé ! Merci de votre contribution.")
            st.balloons()

# 3. PAGE ADMIN / ANALYSE
elif st.session_state.page == "Admin":
    st.button("⬅ RETOUR À L'ACCUEIL", on_click=lambda: changer_page("Accueil"))
    pwd = st.text_input("Mot de passe enquêteur :", type="password")
    if pwd == "admin123":
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM rapports", conn)
        conn.close()
        
        if df.empty: st.info("Aucune donnée.")
        else:
            st.plotly_chart(px.bar(df, x='region', title="Audits par Région"))
            st.plotly_chart(px.box(df, x='hopital', y='attente', title="Temps d'attente par Hôpital"))
            st.dataframe(df)

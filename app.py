import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- VARIABLES D'ÉTAT POUR LA NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
def changer_page(nom): st.session_state.page = nom

# --- DONNÉES NATIONALES ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central", "CHU"],
    "Est": ["Hôpital Régional de Bertoua"],
    "Extrême-Nord": ["Hôpital Régional de Maroua"],
    "Littoral": ["Hôpital Général Douala", "Hôpital Laquintinie"],
    "Nord": ["Hôpital Régional de Garoua"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda"],
    "Ouest": ["Hôpital Régional de Bafoussam"],
    "Sud": ["Hôpital Régional d'Ebolowa"],
    "Sud-Ouest": ["Hôpital Régional de Buea"]
}

# --- DESIGN "PATIENT PLUS" AVEC FOND D'ÉCRAN ---
st.markdown("""
    <style>
    /* Fond d'écran global : Image d'Hôpital */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.8), rgba(0, 43, 92, 0.8)), 
                    url('https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* Bulles d'informations terrain */
    .info-bubble {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px; padding: 20px; color: #1a1a1a; margin-bottom: 20px;
        border-top: 6px solid #e1395f; min-height: 250px;
    }

    /* Bulles de Navigation Cliquables */
    .nav-bubble {
        background-color: rgba(255, 255, 255, 0.15);
        border: 2px solid white; border-radius: 25px; padding: 25px;
        text-align: center; color: white; height: 180px;
        display: flex; flex-direction: column; justify-content: center;
        transition: 0.3s;
    }
    .nav-bubble:hover { background-color: #e1395f; transform: translateY(-5px); }

    /* Boutons stylisés */
    .stButton>button {
        background-color: #e1395f !important; color: white !important;
        border-radius: 50px !important; width: 100%; border: none !important;
        font-weight: bold;
    }
    
    /* Dashboard blanc pour les résultats */
    .dashboard-white {
        background-color: white; padding: 30px; border-radius: 20px;
        color: #1a1a1a; margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('audit_national_complet.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, sexe TEXT, metier TEXT, dob TEXT, domicile TEXT, email TEXT,
                    maladie TEXT, service TEXT, hopital TEXT, region TEXT, experience TEXT,
                    attente INTEGER, attitude_g TEXT, eval_inf TEXT, justif_inf TEXT, eval_med TEXT, justif_med TEXT,
                    rdv_ligne TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- LOGIQUE DES PAGES ---

# 1. PAGE D'ACCUEIL (Avec résultats automatiques)
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:22px;'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>", unsafe_allow_html=True)

    # Bulles d'informations
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="info-bubble">
            <h4>📊 Performance Hospitalière</h4>
            <p>Hôpitaux Régionaux : 4 000 à 6 000 hospitalisations par an.</p>
            <p>Sur 172 hôpitaux publics, seuls 48% remplissent les critères de performance.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="info-bubble">
            <h4>👶 Maternité et Naissances</h4>
            <p>Environ 35,9% des accouchements se font encore à domicile sans assistance médicale au Cameroun.</p>
        </div>""", unsafe_allow_html=True)

    # Bulles de Navigation
    st.markdown("<h3 style='text-align:center;'>NAVIGUER DANS L'APPLICATION</h3>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown('<div class="nav-bubble"><h4>📝 AUDIT</h4><p>Participer à l\'enquête</p></div>', unsafe_allow_html=True)
        st.button("Aller à l'Audit", on_click=lambda: changer_page("Audit"))
    with n2:
        st.markdown('<div class="nav-bubble"><h4>🔐 ADMIN</h4><p>Espace Enquêteur</p></div>', unsafe_allow_html=True)
        st.button("Accéder à l'Espace Admin", on_click=lambda: changer_page("Admin"))
    with n3:
        st.markdown('<div class="nav-bubble"><h4>ℹ️ INFOS</h4><p>À propos du projet</p></div>', unsafe_allow_html=True)
        st.button("Voir les Infos", on_click=lambda: changer_page("Infos"))

    # Affichage des calculs automatiques de l'enquête
    st.markdown("<div class='dashboard-white'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#002b5c;'>📈 RÉSULTATS GLOBAUX DE L'ENQUÊTE</h2>", unsafe_allow_html=True)
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("Les graphiques s'afficheront ici dès que les premiers patients auront répondu.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Audits", len(df))
        m2.metric("Attente Moyenne", f"{round(df['attente'].mean(), 1)} min")
        fav = (len(df[df['rdv_ligne'] == "Oui"]) / len(df)) * 100
        m3.metric("Favorable RDV en ligne", f"{round(fav, 1)}%")

        st.plotly_chart(px.bar(df, x="hopital", y="attente", title="Temps d'attente moyen par hôpital"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 2. PAGE QUESTIONNAIRE (REVENU À LA VERSION COMPLÈTE)
elif st.session_state.page == "Audit":
    st.button("⬅ Retour à l'accueil", on_click=lambda: changer_page("Accueil"))
    st.markdown("<h2>📝 Formulaire d'Audit Patient</h2>", unsafe_allow_html=True)
    
    with st.form("audit_form", clear_on_submit=True):
        st.subheader("1. Identification")
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        age, sexe = c1.number_input("Âge", 0, 110, 25), c2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier, email = c1.text_input("Métier"), c2.text_input("Email")
        dob, domicile = c1.date_input("Date de naissance"), c2.text_input("Lieu de résidence")

        st.subheader("2. Contexte Médical")
        reg = st.selectbox("Région", list(data_cameroun.keys()))
        hop = st.selectbox("Hôpital", data_cameroun[reg])
        service, maladie = st.text_input("Service visité"), st.text_input("Motif/Maladie")
        exp = st.text_area("Racontez brièvement votre expérience")

        st.subheader("3. Évaluation du Personnel")
        attente = st.slider("Temps d'attente (min)", 0, 300, 30)
        attitude = st.selectbox("Attitude globale", ["Médiocre", "Passable", "Satisfaisante", "Excellente"])
        
        ci, cm = st.columns(2)
        e_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
        j_inf = ci.text_area("Justification Infirmières")
        e_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
        j_med = cm.text_area("Justification Médecins")

        st.subheader("4. Suggestions")
        sug = st.text_area("Comment améliorer le service ?")
        rdv = st.radio("Favorable au RDV en ligne ?", ["Oui", "Non"])

        if st.form_submit_button("SOUMETTRE L'AUDIT"):
            conn = get_connection()
            c = conn.cursor()
            c.execute('''INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, domicile, email,
                        maladie, service, hopital, region, experience, attente, attitude_g,
                        eval_inf, justif_inf, eval_med, justif_med, rdv_ligne, suggestions, date_soumission) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                     (nom, prenom, age, sexe, metier, str(dob), domicile, email, maladie, service, hop, reg, 
                      exp, attente, attitude, e_inf, j_inf, e_med, j_med, rdv, sug, datetime.now()))
            conn.commit()
            conn.close()
            st.success("✅ Données enregistrées et envoyées à l'enquêteur.")

# 3. PAGE ENQUÊTEUR (CONNEXION POUR VOIR LES BRUTES)
elif st.session_state.page == "Admin":
    st.button("⬅ Retour à l'accueil", on_click=lambda: changer_page("Accueil"))
    st.markdown("<div class='dashboard-white'>", unsafe_allow_html=True)
    st.subheader("🔐 Connexion Enquêteur")
    
    with st.form("login_admin"):
        nom_e = st.text_input("Votre Nom")
        email_e = st.text_input("Votre Email")
        pwd = st.text_input("Mot de passe", type="password")
        if st.form_submit_button("Se connecter"):
            if pwd == "admin123":
                st.success(f"Bienvenue M. {nom_e}. Voici la base de données brute.")
                conn = get_connection()
                df = pd.read_sql_query("SELECT * FROM rapports", conn)
                conn.close()
                st.dataframe(df)
            else:
                st.error("Mot de passe incorrect.")
    st.markdown("</div>", unsafe_allow_html=True)

# 4. PAGE INFOS
elif st.session_state.page == "Infos":
    st.button("⬅ Retour à l'accueil", on_click=lambda: changer_page("Accueil"))
    st.markdown("<div class='dashboard-white'><h3>ℹ️ À propos de Patient Plus</h3><p>Cette application a été développée dans le cadre de l'audit national hospitalier pour moderniser les services de santé au Cameroun.</p></div>", unsafe_allow_html=True)

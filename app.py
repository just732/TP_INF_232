import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Dashboard National", layout="wide")

# --- NAVIGATION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"

# --- DESIGN "PATIENT PLUS" AVEC IMAGES DE FOND ---
st.markdown("""
    <style>
    /* Image de fond principale (Hôpital Général) */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.75), rgba(0, 43, 92, 0.75)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }

    /* Bulles avec images de fond (Pédiatrie et Maternité) */
    .bubble-pediatrie {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
                    url('https://www.stopblablacam.com/images/k2/items/cache/f7f7b1f1b9f7a7d9a1f1b9f7a7d9a1f1_XL.jpg');
        background-size: cover; padding: 30px; border-radius: 25px; color: #1a1a1a; margin-bottom: 20px; border-left: 10px solid #e1395f;
    }
    .bubble-maternite {
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)),
                    url('https://static.atlantico.fr/sites/default/files/styles/image_744x422/public/images/2013/05/bebe_couveuse.jpg');
        background-size: cover; padding: 30px; border-radius: 25px; color: #1a1a1a; margin-bottom: 20px; border-left: 10px solid #39559e;
    }

    /* Dashboard blanc pour les résultats */
    .dashboard-results {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px; padding: 30px; color: #1a1a1a; margin-top: 30px;
    }

    /* Bouton d'action rouge géant */
    .stButton>button {
        background-color: #e1395f !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 20px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        width: 100%; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('patient_plus_final.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, sexe TEXT, metier TEXT, dob TEXT, domicile TEXT, email TEXT,
                    maladie TEXT, service TEXT, hopital TEXT, experience TEXT, attente INTEGER, attitude_g TEXT,
                    eval_inf TEXT, justif_inf TEXT, eval_med TEXT, justif_med TEXT,
                    rdv_ligne TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- FONCTION DE NAVIGATION ---
def change_page(name):
    st.session_state.page = name

# --- PAGE 1 : ACCUEIL & RÉSULTATS ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:60px;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; opacity:0.9;'>Audit National de la Qualité des Services Hospitaliers au Cameroun</h3>", unsafe_allow_html=True)

    # 1. Objectif
    st.markdown("""
        <div style='background:rgba(255,255,255,0.1); padding:20px; border-radius:15px; text-align:center; margin-bottom:40px;'>
            <p style='font-size:22px;'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. Bulles d'informations terrain
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="bubble-pediatrie">
                <h4>Hôpitaux et Surcharge</h4>
                <p><b>Hospitalisations :</b> Entre 4 000 et 6 000 par an dans les hôpitaux régionaux.</p>
                <p><b>Performance :</b> Seuls 48% des 172 hôpitaux publics sont jugés performants.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="bubble-maternite">
                <h4>Accouchements et Maternité</h4>
                <p><b>Admission :</b> 35,9% des accouchements se font encore à domicile sans assistance.</p>
                <p>Cela impacte directement la sécurité sanitaire des nouveau-nés.</p>
            </div>
        """, unsafe_allow_html=True)

    # 3. AFFICHAGE DES RÉSULTATS DE L'ENQUÊTE (Automatique)
    st.markdown("<div class='dashboard-results'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#39559e;'>📊 RÉSULTATS DE L'AUDIT EN TEMPS RÉEL</h2>", unsafe_allow_html=True)
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("Aucun audit n'a encore été soumis. Les résultats s'afficheront ici après la première validation.")
    else:
        # Métriques Rapides
        m1, m2, m3 = st.columns(3)
        m1.metric("Audits Complétés", len(df))
        m2.metric("Attente Moyenne (min)", f"{round(df['attente'].mean(), 1)}")
        taux = (len(df[df['rdv_ligne'] == "Oui"]) / len(df)) * 100
        m3.metric("Favorable RDV Ligne", f"{round(taux, 1)}%")

        # Graphiques descriptifs
        fig_attente = px.bar(df.groupby('hopital')['attente'].mean().reset_index(), 
                             x='hopital', y='attente', title="Temps d'attente moyen par établissement")
        st.plotly_chart(fig_attente, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 4. BOUTON POUR REMPLIR LE FORMULAIRE
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.button("📝 CLIQUEZ ICI POUR REMPLIR L'AUDIT", on_click=lambda: change_page("Formulaire"))

# --- PAGE 2 : FORMULAIRE D'AUDIT ---
elif st.session_state.page == "Formulaire":
    st.button("⬅ Retour à l'accueil", on_click=lambda: change_page("Accueil"))
    st.markdown("<h1 style='text-align:center;'>FORMULAIRE D'AUDIT</h1>", unsafe_allow_html=True)
    
    with st.form("audit_form"):
        st.subheader("1. Identification")
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        age, sexe = c1.number_input("Âge", 0, 110, 25), c2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier, dob = c1.text_input("Métier"), c2.date_input("Date de naissance")
        dom, email = c1.text_input("Lieu de résidence"), c2.text_input("Adresse Email")

        st.subheader("2. Contexte et Soins")
        c3, c4 = st.columns(2)
        hopital = c3.selectbox("Hôpital", ["Hôpital Général", "Hôpital Central", "Hôpital de Laquintinie", "Hôpital de District"])
        service, maladie = c4.text_input("Service visité"), st.text_input("Maladie / Motif de consultation")
        exp = st.text_area("Racontez brièvement votre expérience")

        st.subheader("3. Évaluation")
        attente, attitude = st.slider("Attente (min)", 0, 300, 30), st.selectbox("Attitude globale", ["Insuffisante", "Passable", "Satisfaisante", "Excellente"])
        
        c_i, c_m = st.columns(2)
        e_inf, j_inf = c_i.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"]), c_i.text_area("Justification (Infirmières)")
        e_med, j_med = c_m.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"]), c_m.text_area("Justification (Médecins)")

        st.subheader("4. Recommandations")
        rdv = st.radio("Favorable au RDV en ligne avec un médecin ?", ["Oui", "Non"])
        sug = st.text_area("Vos propositions pour améliorer la qualité du service :")

        if st.form_submit_button("VALIDER ET ENVOYER L'AUDIT"):
            if nom and prenom and email:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, domicile, email,
                            maladie, service, hopital, experience, attente, attitude_g,
                            eval_inf, justif_inf, eval_med, justif_med, rdv_ligne, suggestions, date_soumission) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, age, sexe, metier, str(dob), dom, email, maladie, service, hopital, 
                          exp, attente, attitude, e_inf, j_inf, e_med, j_med, rdv, sug, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ Audit envoyé ! Les statistiques sur la page d'accueil ont été mises à jour.")
                # Retour automatique à l'accueil
                change_page("Accueil")
                st.rerun()
            else:
                st.error("Veuillez remplir les informations obligatoires.")

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National Cameroun", layout="wide")

# --- DESIGN PERSONNALISÉ (STYLE PATIENT PLUS) ---
# Note : Remplacez les liens 'URL_IMAGE_X' par les liens de vos images une fois sur GitHub
st.markdown("""
    <style>
    /* Image de fond (Image 3 : Hôpital Général) */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.7), rgba(0, 43, 92, 0.7)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }

    /* Style des bulles d'information (Cartes) */
    .info-bubble {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 25px;
        color: #1a1a1a;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        border-top: 8px solid #e1395f;
    }
    .info-bubble h4 { color: #39559e; font-weight: bold; }
    .info-bubble img {
        width: 100%;
        border-radius: 15px;
        margin-bottom: 15px;
        height: 200px;
        object-fit: cover;
    }

    /* Style du texte d'objectif */
    .goal-text {
        font-size: 26px !important;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin-bottom: 30px;
    }

    /* Formulaire */
    label { color: white !important; font-weight: bold; }
    .stTextInput input, .stTextArea textarea { border-radius: 10px !important; }

    /* Bouton rouge Patient Plus */
    .stButton>button {
        background-color: #e1395f !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 15px 30px !important;
        width: 100%;
        font-weight: bold !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_cameroun_v6.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, sexe TEXT, metier TEXT, 
                    dob TEXT, domicile TEXT, email TEXT,
                    maladie TEXT, service TEXT, hopital TEXT, experience TEXT,
                    attente INTEGER, attitude_g TEXT,
                    eval_inf TEXT, justif_inf TEXT, eval_med TEXT, justif_med TEXT,
                    rdv_ligne TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- NAVIGATION ---
page = st.sidebar.radio("Navigation", ["🏠 Accueil", "📝 Formulaire d'Audit", "📊 Statistiques"])

# --- PAGE 1 : ACCUEIL ---
if page == "🏠 Accueil":
    st.markdown("<h1 style='text-align:center;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="goal-text">
            Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class="info-bubble">
                <img src="https://www.stopblablacam.com/images/k2/items/cache/f7f7b1f1b9f7a7d9a1f1b9f7a7d9a1f1_XL.jpg">
                <h4>Hôpitaux et Consultations</h4>
                <ul>
                    <li><b>Hôpitaux Régionaux :</b> Enregistrent entre 4 000 et 6 000 hospitalisations par an (surcharge critique).</li>
                    <li><b>Performance :</b> Sur 172 hôpitaux publics, seulement 48% remplissent les critères de "bonne performance".</li>
                    <li><b>Enfants (-5 ans) :</b> Les consultations externes sont un indicateur majeur de suivi de santé nationale.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="info-bubble">
                <img src="https://static.atlantico.fr/sites/default/files/styles/image_744x422/public/images/2013/05/bebe_couveuse.jpg">
                <h4>Services de Maternité</h4>
                <p><b>Admission Institutionnelle :</b> Environ 35,9% des accouchements se font encore à domicile sans assistance médicale au Cameroun.</p>
                <p>Cela réduit considérablement le taux d'admission sécurisée dans les maternités hospitalières.</p>
            </div>
        """, unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE ---
elif page == "📝 Formulaire d'Audit":
    st.markdown("<h2 style='text-align:center;'>Questionnaire de Qualité Hospitalière</h2>", unsafe_allow_html=True)
    
    with st.form("audit_form"):
        st.subheader("1. Identification")
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        age = c1.number_input("Âge", 0, 110, 25)
        sexe = c2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier = c1.text_input("Métier")
        dob = c2.date_input("Date de naissance")
        domicile = c1.text_input("Lieu de résidence")
        email = c2.text_input("Adresse Email")

        st.subheader("2. Contexte Médical")
        c3, c4 = st.columns(2)
        hopital = c3.selectbox("Établissement", ["Hôpital Général", "Hôpital Central", "Hôpital de Laquintinie", "Hôpital de District"])
        service = c4.text_input("Service (ex: Urgences, Maternité...)")
        maladie = st.text_input("Maladie ou motif de consultation")
        experience = st.text_area("Racontez votre expérience")

        st.subheader("3. Évaluation du Personnel")
        attente = st.slider("Temps d'attente (min)", 0, 300, 30)
        attitude_g = st.selectbox("Attitude globale", ["Insuffisante", "Moyenne", "Satisfaisante", "Excellente"])
        
        ci, cm = st.columns(2)
        e_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
        j_inf = ci.text_area("Justification (Infirmières)")
        e_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
        j_med = cm.text_area("Justification (Médecins)")

        st.subheader("4. Recommandations")
        rdv = st.radio("Prendre rendez-vous en ligne avec un médecin spécifique vous conviendrait-il ?", ["Oui", "Non"])
        sug = st.text_area("Comment faire pour améliorer la qualité du service ?")

        if st.form_submit_button("SOUMETTRE MON AUDIT"):
            if nom and prenom and email:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, domicile, email,
                            maladie, service, hopital, experience, attente, attitude_g,
                            eval_inf, justif_inf, eval_med, justif_med, rdv_ligne, suggestions, date_soumission) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, age, sexe, metier, str(dob), domicile, email, maladie, service, 
                          hopital, experience, attente, attitude_g, e_inf, j_inf, e_med, j_med, rdv, sug, datetime.now()))
                conn.commit()
                conn.close()
                st.success("Données enregistrées. Merci de contribuer à l'amélioration de la santé !")

# --- PAGE 3 : ANALYSE ---
elif page == "📊 Statistiques":
    st.markdown("<h2 style='text-align:center;'>Analyse Descriptive</h2>", unsafe_allow_html=True)
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        st.plotly_chart(px.bar(df, x='hopital', y='attente', color='attitude_g', title="Attente par Établissement"))
        st.subheader("Détails des suggestions")
        st.dataframe(df[['hopital', 'suggestions', 'date_soumission']])

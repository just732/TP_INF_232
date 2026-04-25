import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide")

# --- INITIALISATION DE LA NAVIGATION ---
if "page_nav" not in st.session_state:
    st.session_state.page_nav = "🏠 Accueil"

# --- DESIGN "PATIENT PLUS" AVEC IMAGES EN FOND ---
st.markdown(
    """
    <style>
    /* Image 3 en fond d'écran total de l'application */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.75), rgba(0, 43, 92, 0.75)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }

    /* Style du texte d'objectif */
    .goal-text {
        font-size: 26px !important;
        font-weight: bold;
        text-align: center;
        padding: 30px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        margin-bottom: 40px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* Bulle 1 avec l'image 1 en fond d'écran */
    .bubble-img-1 {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url('https://www.stopblablacam.com/images/k2/items/cache/f7f7b1f1b9f7a7d9a1f1b9f7a7d9a1f1_XL.jpg');
        background-size: cover;
        background-position: center;
        border-radius: 25px;
        padding: 30px;
        color: white !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }

    /* Bulle 2 avec l'image 2 en fond d'écran */
    .bubble-img-2 {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
                    url('https://static.atlantico.fr/sites/default/files/styles/image_744x422/public/images/2013/05/bebe_couveuse.jpg');
        background-size: cover;
        background-position: center;
        border-radius: 25px;
        padding: 30px;
        color: white !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }

    /* Forcer la couleur blanche pour les titres dans les bulles images */
    .bubble-img-1 h3, .bubble-img-2 h3 {
        color: #e1395f !important;
        font-weight: bold;
    }

    /* Formulaire */
    label { color: white !important; font-weight: bold; }
    .stTextInput input, .stTextArea textarea { border-radius: 10px !important; }

    /* Bouton rouge Patient Plus géant en bas de page */
    .big-red-button > button {
        background-color: #e1395f !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 20px 40px !important;
        width: 100% !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(225, 57, 95, 0.4);
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect("audit_cameroun_v7.db", check_same_thread=False)


def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, sexe TEXT, metier TEXT, 
                    dob TEXT, domicile TEXT, email TEXT,
                    maladie TEXT, service TEXT, hopital TEXT, experience TEXT,
                    attente INTEGER, attitude_g TEXT,
                    eval_inf TEXT, justif_inf TEXT, eval_med TEXT, justif_med TEXT,
                    rdv_ligne TEXT, suggestions TEXT, date_soumission DATETIME)"""
    )
    conn.commit()
    conn.close()


init_db()

# --- BARRE LATÉRALE ---
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Accueil", "📝 Formulaire d'Audit", "📊 Statistiques"],
    key="nav_radio",
)

# Synchronisation avec le bouton de la page d'accueil
if st.session_state.page_nav != page:
    st.session_state.page_nav = page

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page_nav == "🏠 Accueil":
    st.markdown(
        "<h1 style='text-align:center; font-size:50px; color:white;'>PATIENT PLUS</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="goal-text">
            Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="bubble-img-1">
                <h3>Hôpitaux et Consultations</h3>
                <p><b>Hôpitaux Régionaux :</b> Enregistrent entre 4 000 et 6 000 hospitalisations par an, ce qui est jugé très élevé par rapport à leur capacité d'accueil.</p>
                <p><b>Performance :</b> Sur 172 hôpitaux publics, seulement 48% remplissent les critères de "bonne performance hospitalière".</p>
                <p><b>Enfants (-5 ans) :</b> La fréquentation des services externes est un indicateur de suivi majeur.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="bubble-img-2">
                <h3>Services de Maternité</h3>
                <p><b>Admission Institutionnelle :</b> Environ 35,9% des accouchements se font encore à domicile sans assistance médicale au Cameroun.</p>
                <p>Ce phénomène réduit le taux d'admission institutionnelle pour les maternités et augmente les risques.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Bouton d'action en bas de page pour aller au formulaire
    st.markdown('<div class="big-red-button">', unsafe_allow_html=True)
    if st.button("📝 Commencer l'audit (Remplir le formulaire)"):
        st.session_state.page_nav = "📝 Formulaire d'Audit"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE ---
elif st.session_state.page_nav == "📝 Formulaire d'Audit":
    st.markdown(
        "<h2 style='text-align:center;'>Questionnaire de Qualité Hospitalière</h2>",
        unsafe_allow_html=True,
    )

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
        hopital = c3.selectbox(
            "Établissement",
            [
                "Hôpital Général",
                "Hôpital Central",
                "Hôpital de Laquintinie",
                "Hôpital de District",
            ],
        )
        service = c4.text_input("Service (ex: Urgences, Maternité...)")
        maladie = st.text_input("Maladie ou motif de consultation")
        experience = st.text_area("Racontez votre expérience")

        st.subheader("3. Évaluation du Personnel")
        attente = st.slider("Temps d'attente (min)", 0, 300, 30)
        attitude_g = st.selectbox(
            "Attitude globale",
            ["Insuffisante", "Moyenne", "Satisfaisante", "Excellente"],
        )

        ci, cm = st.columns(2)
        e_inf = ci.select_slider(
            "Note Infirmières", options=["1", "2", "3", "4", "5"]
        )
        j_inf = ci.text_area("Justification (Infirmières)")
        e_med = cm.select_slider(
            "Note Médecins", options=["1", "2", "3", "4", "5"]
        )
        j_med = cm.text_area("Justification (Médecins)")

        st.subheader("4. Recommandations")
        rdv = st.radio(
            "Prendre rendez-vous en ligne avec un médecin spécifique vous conviendrait-il ?",
            ["Oui", "Non"],
        )
        sug = st.text_area(
            "Comment faire pour améliorer la qualité du service ?"
        )

        if st.form_submit_button("SOUMETTRE MON AUDIT"):
            if nom and prenom and email:
                conn = get_connection()
                c = conn.cursor()
                c.execute(
                    """INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, domicile, email,
                            maladie, service, hopital, experience, attente, attitude_g,
                            eval_inf, justif_inf, eval_med, justif_med, rdv_ligne, suggestions, date_soumission) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        nom,
                        prenom,
                        age,
                        sexe,
                        metier,
                        str(dob),
                        domicile,
                        email,
                        maladie,
                        service,
                        hopital,
                        experience,
                        attente,
                        attitude_g,
                        e_inf,
                        j_inf,
                        e_med,
                        j_med,
                        rdv,
                        sug,
                        datetime.now(),
                    ),
                )
                conn.commit()
                conn.close()
                st.success("Données enregistrées avec succès !")

# --- PAGE 3 : STATISTIQUES ---
elif st.session_state.page_nav == "📊 Statistiques":
    st.markdown(
        "<h2 style='text-align:center;'>Analyse Descriptive</h2>",
        unsafe_allow_html=True,
    )
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        st.plotly_chart(
            px.bar(
                df,
                x="hopital",
                y="attente",
                color="attitude_g",
                title="Attente par Établissement",
            )
        )
        st.subheader("Détails des suggestions d'amélioration")
        st.dataframe(df[["hopital", "suggestions", "date_soumission"]])

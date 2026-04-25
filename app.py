import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit Cameroun", layout="wide")

# --- DESIGN "PATIENT PLUS" (Inspiré de l'image) ---
st.markdown(f"""
    <style>
    /* Palette de couleurs de l'image */
    :root {{
        --main-blue: #39559e;
        --light-blue: #5774ba;
        --accent-red: #e1395f;
        --soft-gray: #d0ced0;
        --white: #ffffff;
    }}

    .stApp {{
        background: linear-gradient(180deg, var(--main-blue) 0%, var(--light-blue) 100%);
        color: var(--white);
    }}

    /* Style des conteneurs (Bulles/Cartes) */
    .app-card {{
        background-color: var(--white);
        border-radius: 20px;
        padding: 25px;
        color: #333;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }}

    /* Logo et Titre */
    .logo-container {{
        text-align: center;
        margin-bottom: 30px;
    }}
    .logo-heart {{
        font-size: 80px;
        color: var(--white);
    }}

    /* Formulaire Style */
    label {{ color: var(--white) !important; font-weight: bold; font-size: 16px; }}
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {{
        border-radius: 10px !important;
    }}

    /* Boutons Rouges (Comme le bouton LOG IN / SIGN UP) */
    .stButton>button {{
        background-color: var(--accent-red) !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 15px 40px !important;
        font-weight: bold !important;
        width: 100%;
        font-size: 18px !important;
        text-transform: uppercase;
    }}
    
    h1, h2, h3 {{ color: var(--white) !important; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('patient_plus_cmr.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, sexe TEXT, 
                    metier TEXT, date_naissance TEXT, domicile TEXT, email TEXT,
                    raison_visite TEXT, maladie TEXT, nom_hopital TEXT, service_hopital TEXT,
                    temps_urgence INTEGER, attitude_globale TEXT,
                    eval_infirmieres TEXT, justif_infirmieres TEXT,
                    eval_medecins TEXT, justif_medecins TEXT,
                    rdv_ligne TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- NAVIGATION STYLE MOBILE ---
st.sidebar.markdown("<h1 style='color:white;'>Patient Plus</h1>", unsafe_allow_html=True)
page = st.sidebar.radio("Navigation", ["🏠 Accueil", "📝 Formulaire d'Audit", "📊 Statistiques Cameroun"])

# --- PAGE 1 : ACCUEIL ---
if page == "🏠 Accueil":
    st.markdown("""
        <div class="logo-container">
            <div class="logo-heart">🤍</div>
            <h1 style='margin-top:0;'>Patient Plus</h1>
            <p style='font-style: italic;'> "Where compassion and healthcare meet" </p>
        </div>
        
        <div class="app-card" style="background-color:rgba(255,255,255,0.9);">
            <h3 style="color:#39559e !important;">Objectif de l'application</h3>
            <p style="font-size:18px; color:#444;">
                Cette application a pour but d’améliorer la qualité du traitement de service dans nos services d’urgence et hospitaliers du pays. 
                Elle permet à chaque citoyen de devenir acteur de la réforme sanitaire.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🇨🇲 Statistiques de Santé au Cameroun")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="app-card">
                <h2 style="color:#e1395f !important;">65%</h2>
                <p style="color:#444;">des patients sont traités dans les hôpitaux publics chaque année au Cameroun.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="app-card">
                <h2 style="color:#39559e !important;">35%</h2>
                <p style="color:#444;">des consultations concernent les services d'urgence et les maternités.</p>
            </div>
        """, unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE D'AUDIT ---
elif page == "📝 Formulaire d'Audit":
    st.markdown("<h1>Audit de Qualité Hospitalière</h1>", unsafe_allow_html=True)
    
    with st.form("audit_form", clear_on_submit=True):
        st.markdown("### 👤 Identification du Patient")
        col1, col2 = st.columns(2)
        nom = col1.text_input("Nom")
        prenom = col2.text_input("Prénom")
        age = col1.number_input("Âge", 0, 120, 25)
        sexe = col2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier = col1.text_input("Métier")
        dob = col2.date_input("Date de naissance")
        domicile = col1.text_input("Lieu de résidence (Ville/Quartier)")
        email = col2.text_input("Adresse Email")

        st.markdown("### 🏥 Contexte Médical")
        c3, c4 = st.columns(2)
        hopital = c3.selectbox("Hôpital fréquenté", ["Hôpital Central", "Hôpital Général", "Hôpital de Laquintinie", "Hôpital de District", "Autre"])
        service = c4.text_input("Service (ex: Urgences, Cardiologie, Maternité...)")
        maladie = st.text_input("Maladie ou motif de consultation")
        raison_visite = st.text_area("Racontez brièvement votre expérience")

        st.markdown("### ⭐ Évaluation du Personnel")
        t_attente = st.slider("Temps d'attente (en minutes)", 0, 300, 30)
        attitude = st.selectbox("Attitude globale du personnel", ["Médiocre", "Passable", "Satisfaisante", "Excellente"])
        
        col_inf, col_med = st.columns(2)
        with col_inf:
            e_inf = st.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
            j_inf = st.text_area("Justification (Infirmières)")
        with col_med:
            e_med = st.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
            j_med = st.text_area("Justification (Médecins)")

        st.markdown("### 🌐 Digitalisation & Conseils")
        rdv_ligne = st.radio("Prendre rendez-vous en ligne avec un médecin spécifique vous conviendrait-il ?", ["Oui", "Non"])
        suggestions = st.text_area("Comment faire pour améliorer la qualité du service selon vous ?")

        if st.form_submit_button("SOUMETTRE MON AUDIT"):
            if nom and prenom and email:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, age, sexe, metier, date_naissance, domicile, email,
                            raison_visite, maladie, nom_hopital, service_hopital, temps_urgence, attitude_globale,
                            eval_infirmieres, justif_infirmieres, eval_medecins, justif_medecins,
                            rdv_ligne, suggestions, date_soumission) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, age, sexe, metier, str(dob), domicile, email, raison_visite, maladie, 
                          hopital, service, t_attente, attitude, e_inf, j_inf, e_med, j_med, rdv_ligne, suggestions, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ Audit transmis avec succès ! Merci de contribuer à la santé au Cameroun.")
            else:
                st.error("Veuillez remplir les champs obligatoires (Nom, Prénom, Email).")

# --- PAGE 3 : STATISTIQUES ---
elif page == "📊 Statistiques Cameroun":
    st.markdown("<h1>Résultats de l'Audit National</h1>", unsafe_allow_html=True)
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée collectée pour le moment.")
    else:
        # Style des métriques dans des cartes
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="app-card"><h4>Audits</h4><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="app-card"><h4>Attente Moy.</h4><h2>{round(df["temps_urgence"].mean(), 1)}m</h2></div>', unsafe_allow_html=True)
        with m3:
            fav = (len(df[df['rdv_ligne'] == "Oui"]) / len(df)) * 100
            st.markdown(f'<div class="app-card"><h4>RDV Ligne</h4><h2>{round(fav, 1)}%</h2></div>', unsafe_allow_html=True)

        st.divider()
        fig = px.bar(df, x="nom_hopital", y="temps_urgence", color="sexe", title="Temps d'attente par Hôpital et Sexe")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Suggestions d'amélioration collectées")
        st.dataframe(df[['nom_hopital', 'suggestions', 'date_soumission']], use_container_width=True)

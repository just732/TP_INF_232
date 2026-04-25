import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National Cameroun", layout="wide")

# --- DESIGN PERSONNALISÉ (Style Moderne avec Images en Fond) ---
st.markdown("""
    <style>
    /* Fond global : Fond d'écran de l'hôpital */
    .stApp {
        background-image: url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg'); /* Image de fond principale */
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white; /* Police blanche sur fond sombre */
    }
    /* Masque pour rendre le texte lisible sur l'image */
    .app-content {
        background-color: rgba(0, 43, 92, 0.85); /* Fond bleu foncé semi-transparent */
        padding: 40px;
        border-radius: 25px;
        margin: 20px 0;
    }

    /* Style des bulles d'information avec image en fond */
    .info-bubble {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        color: #1a1a1a;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        border-top: 6px solid #e1395f; /* Touche rouge pour l'importance */
        height: 320px; /* Hauteur fixe pour un alignement */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .info-bubble h4 { 
        color: #39559e; 
        font-weight: bold; 
        font-size: 20px;
        margin-bottom: 10px;
    }
    .info-bubble img {
        width: 100%;
        height: 120px; /* Hauteur réduite pour l'image en fond de bulle */
        object-fit: cover;
        border-radius: 15px;
        margin-bottom: 10px;
    }

    /* Section d'accueil avec objectif et titre */
    .hero-section {
        text-align: center;
        padding: 50px 0;
    }
    .hero-section h1 { font-size: 55px !important; font-weight: 700; margin-bottom: 10px; }
    .hero-section p { font-size: 22px !important; font-weight: 500; max-width: 800px; margin: 0 auto; }

    /* Bouton "Accéder au formulaire" */
    .cta-button {
        display: block;
        width: fit-content;
        margin: 30px auto 0 auto;
        padding: 12px 30px;
        background-color: #e1395f !important;
        color: white !important;
        border-radius: 50px !important;
        text-decoration: none;
        font-size: 18px;
        font-weight: bold;
    }

    /* Formulaire */
    label { color: white !important; font-weight: bold; }
    .stTextInput input, .stTextArea textarea, .stSelectbox div div div { 
        background-color: rgba(255, 255, 255, 0.8) !important; 
        color: black !important;
        border-radius: 10px !important;
    }
    /* Bouton soumettre du formulaire */
    .stButton>button {
        background-color: #39559e !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('patient_plus_audit_v7.db', check_same_thread=False)

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
    st.markdown("""
        <div class="hero-section">
            <h1>PATIENT PLUS</h1>
            <p>Votre feedback, notre priorité pour l'amélioration continue des services de santé au Cameroun.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='app-content'>", unsafe_allow_html=True)
    
    st.subheader("Objectifs Stratégiques de l'Audit National")
    st.markdown("""
        <p style="font-size: 18px; max-width: 900px; margin: 10px auto;">
        Notre mission est de recueillir des données précises sur votre expérience dans les établissements de santé. 
        Les informations collectées serviront à identifier les points d'amélioration clés concernant les urgences, la qualité des soins, et l'adoption des nouvelles technologies comme les rendez-vous en ligne.
        </p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="info-bubble">
                <img src="https://www.stopblablacam.com/images/k2/items/cache/f7f7b1f1b9f7a7d9a1f1b9f7a7d9a1f1_XL.jpg">
                <h4>Données d'Efficacité</h4>
                <ul>
                    <li><b>Taux d'Hospitalisation :</b> 4 000-6 000/an dans les hôpitaux régionaux (surcharge).</li>
                    <li><b>Performance :</b> 48% des hôpitaux publics jugés performants.</li>
                    <li><b>Suivi :</b> Importance des consultations pédiatriques externes.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="info-bubble">
                <img src="https://static.atlantico.fr/sites/default/files/styles/image_744x422/public/images/2013/05/bebe_couveuse.jpg">
                <h4>Santé Maternelle et Infantile</h4>
                <p><b>Risque à domicile :</b> 35,9% des naissances se font sans assistance médicale.</p>
                <p>Priorité à la sécurité et au suivi institutionnel des mères et nouveau-nés.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;'><a href='#page-formulaire' class='cta-button'>Participer à l'Audit</a></div>", unsafe_allow_html=True)
    
    # Ajout d'un placeholder pour le formulaire afin de pouvoir y accéder via le lien.
    # Il sera toujours caché tant que l'utilisateur n'est pas sur la page formulaire.
    with st.container():
        st.markdown("<a name='page-formulaire'></a>", unsafe_allow_html=True) # Ancre pour le lien
        st.write("") # Ligne vide pour l'espacement

# --- PAGE 2 : FORMULAIRE D'AUDIT ---
if page == "📝 Formulaire d'Audit":
    st.markdown("<h1 style='text-align:center;'>Formulaire d'Audit Patient</h1>", unsafe_allow_html=True)
    
    with st.form("audit_form"):
        st.subheader("I. Informations Personnelles")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom de famille")
        prenom = c2.text_input("Prénom")
        age = c1.number_input("Âge", min_value=0, max_value=120, value=25)
        sexe = c2.selectbox("Sexe", ["Masculin", "Féminin", "Autre"])
        metier = c1.text_input("Profession")
        dob = c2.date_input("Date de naissance")
        domicile = c1.text_input("Lieu de résidence (Ville/Quartier)")
        email = c2.text_input("Adresse Email")

        st.subheader("II. Contexte de la Consultation")
        c3, c4 = st.columns(2)
        hopital = c3.selectbox("Hôpital visité", ["Hôpital Général", "CHU Central", "Hôpital de District", "Clinique Privée", "Autre"])
        service = c4.text_input("Service concerné (ex: Urgences, Maternité, Cardiologie)")
        maladie = st.text_input("Motif principal de la visite (Maladie/Symptômes)")
        experience = st.text_area("Décrivez votre expérience générale")

        st.subheader("III. Évaluation du Personnel")
        attente = st.slider("Temps d'attente aux urgences (minutes)", 0, 300, 30)
        attitude_g = st.selectbox("Attitude globale du personnel", ["Insuffisante", "Moyenne", "Satisfaisante", "Excellente"])
        
        col_inf, col_med = st.columns(2)
        with col_inf:
            e_inf = st.select_slider("Évaluation Infirmières", options=["1", "2", "3", "4", "5"])
            j_inf = st.text_area("Justification (Infirmières)")
        with col_med:
            e_med = st.select_slider("Évaluation Médecins", options=["1", "2", "3", "4", "5"])
            j_med = st.text_area("Justification (Médecins)")

        st.subheader("IV. Recommandations et Digitalisation")
        rdv_ligne = st.radio("Préférence pour un rendez-vous en ligne avec un médecin spécifique ?", ["Favorable", "Défavorable"])
        suggestions = st.text_area("Propositions concrètes pour améliorer le service")

        if st.form_submit_button("SOUMETTRE L'AUDIT"):
            if nom and prenom and email and suggestions: # Vérification des champs essentiels
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, domicile, email,
                            maladie, service, hopital, experience, attente, attitude_g,
                            eval_inf, justif_inf, eval_med, justif_med, rdv_ligne, suggestions, date_soumission) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, age, sexe, metier, str(dob), domicile, email, maladie, service, 
                          hopital, experience, attente, attitude_g, e_inf, j_inf, e_med, j_med, rdv_ligne, suggestions, datetime.now()))
                conn.commit()
                conn.close()
                st.success("Données enregistrées. Merci pour votre contribution à l'amélioration du système de santé.")
                st.balloons() # Effet visuel pour la réussite
            else:
                st.error("Veuillez compléter les informations d'identification (Nom, Prénom, Email) et vos suggestions.")

# --- PAGE 3 : ANALYSE DES DONNÉES ---
elif page == "📊 Statistiques":
    st.markdown("<h1 style='text-align:center;'>Tableau de Bord National</h1>", unsafe_allow_html=True)
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.warning("Aucune donnée n'a encore été collectée pour l'analyse.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Nombre d'Audits", len(df))
        m2.metric("Attente Moyenne", f"{round(df['temps_urgence'].mean(), 1)} min")
        rdv_pos = (len(df[df['rdv_ligne'] == "Oui"]) / len(df)) * 100
        m3.metric("Favorable RDV Ligne", f"{round(rdv_pos, 1)}%")

        st.divider()
        
        st.subheader("Analyse des Temps d'Attente par Hôpital")
        fig = px.bar(df.groupby('hopital')['attente'].mean().reset_index(), 
                     x='hopital', y='attente', 
                     title="Temps moyen d'attente aux urgences",
                     color_discrete_sequence=['#39559e'])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Synthèse des Suggestions d'Amélioration")
        st.dataframe(df[['hopital', 'suggestions', 'date_soumission']])

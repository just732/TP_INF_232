import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Audit Qualité Hospitalière", layout="wide")

# --- DESIGN "QUANTITATIVE METHODS" (ÉPURÉ ET CLAIR) ---
st.markdown("""
    <style>
    /* Fond global de l'application (Gris très clair pour le confort visuel) */
    .stApp {
        background-color: #f4f7f9;
        color: #1a1a1a;
    }
    
    /* Bannière Bleue du haut (comme sur l'image) */
    .header-banner {
        background-color: #002b5c;
        padding: 3rem;
        border-radius: 0 0 30px 30px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    
    /* Cartes blanches (les 3 étapes de l'image) */
    .card-container {
        display: flex;
        justify-content: space-around;
        gap: 20px;
        margin-bottom: 2rem;
    }
    .method-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        flex: 1;
        border-top: 5px solid #0056b3;
    }
    .card-number {
        background-color: #002b5c;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-block;
        line-height: 30px;
        margin-bottom: 10px;
    }

    /* FORMULAIRE : Rendre le texte écrit très visible */
    input, textarea, select {
        color: #000000 !important; /* Texte noir quand on écrit */
        background-color: #ffffff !important; /* Fond blanc des champs */
    }
    label {
        color: #002b5c !important; /* Libellés en bleu foncé */
        font-weight: bold !important;
    }

    /* Bouton principal */
    .stButton>button {
        background-color: #002b5c;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_data.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, domicile TEXT, metier TEXT,
                    raison_visite TEXT, nom_hopital TEXT, temps_urgence INTEGER,
                    qualite_soins TEXT, attitude_personnel TEXT, efficacite_travail TEXT,
                    rdv_medecin_ligne TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- BARRE LATÉRALE ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/684/684262.png", width=100)
st.sidebar.title("Menu Audit")
menu = st.sidebar.radio("Navigation", ["🏠 Page d'accueil", "📝 Formulaire d'Audit", "📊 Dashboard Analyse"])

# --- PAGE 1 : ACCUEIL (STYLE IMAGE "QUANTITATIVE METHODS") ---
if menu == "🏠 Page d'accueil":
    st.markdown('<div class="header-banner"><h1>Quantitative Audit Methods</h1><p>Système de gestion et d\'analyse de la qualité hospitalière</p></div>', unsafe_allow_html=True)
    
    # Les 3 cartes comme sur votre image
    st.markdown("""
    <div class="card-container">
        <div class="method-card">
            <div class="card-number">1</div>
            <h4>Identification</h4>
            <p style="color:#666;">Collecte des données démographiques et profil patient.</p>
        </div>
        <div class="method-card">
            <div class="card-number">2</div>
            <h4>Audit Clinique</h4>
            <p style="color:#666;">Mesure de la qualité des soins et du comportement du personnel.</p>
        </div>
        <div class="method-card">
            <div class="card-number">3</div>
            <h4>Optimisation</h4>
            <p style="color:#666;">Analyse du besoin en digitalisation (Rendez-vous en ligne).</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 Cet audit vise à améliorer les services hospitaliers en transformant vos réponses en indicateurs de performance (KPI).")

# --- PAGE 2 : FORMULAIRE (LISIBLE ET CLAIR) ---
elif menu == "📝 Formulaire d'Audit":
    st.markdown("<h2 style='color:#002b5c;'>📝 Questionnaire d'Audit Hospitalier</h2>", unsafe_allow_html=True)
    
    with st.form("audit_form", clear_on_submit=True):
        st.subheader("👤 Informations Personnelles")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom de famille")
        prenom = c2.text_input("Prénom")
        domicile = c1.text_input("Lieu de domicile (Quartier/Ville)")
        metier = c2.text_input("Profession actuelle")
        
        st.subheader("🏥 Contexte de la Visite")
        raison = st.text_area("Raison de la visite (De quoi souffriez-vous ?)")
        hopital = st.selectbox("Hôpital visité", ["Hôpital Général", "CHU Central", "Clinique de la Paix", "Hôpital de District"])
        
        st.subheader("⭐ Évaluation des Services")
        col1, col2 = st.columns(2)
        with col1:
            t_urgence = st.number_input("Temps d'attente aux urgences (en minutes)", 0, 300, 15)
            soins = st.select_slider("Qualité globale des soins reçus", options=["Médiocre", "Passable", "Satisfaisant", "Excellent"])
        with col2:
            attitude = st.selectbox("Attitude du personnel", ["Impoli", "Indifférent", "Professionnel", "Très accueillant"])
            travail = st.radio("Façon de travailler du personnel", ["Désorganisée", "Moyenne", "Très organisée"])
        
        st.subheader("🌐 Digitalisation des Services")
        # LA QUESTION SPÉCIFIQUE
        rdv_ligne = st.radio("Vous conviendrait-il de prendre rendez-vous en ligne avec un médecin spécifique de cet hôpital ?", 
                            ["Oui, ce serait préférable", "Non, je préfère le système actuel"])

        if st.form_submit_button("SOUMETTRE L'AUDIT"):
            if nom and prenom and raison:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, domicile, metier, raison_visite, 
                            nom_hopital, temps_urgence, qualite_soins, attitude_personnel, 
                            efficacite_travail, rdv_medecin_ligne, date_soumission) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, domicile, metier, raison, hopital, t_urgence, 
                          soins, attitude, travail, rdv_ligne, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ Vos données ont été enregistrées. Merci pour votre contribution !")
            else:
                st.error("Veuillez remplir tous les champs d'identification et la raison de la visite.")

# --- PAGE 3 : ANALYSE (DASHBOARD) ---
elif menu == "📊 Dashboard Analyse":
    st.markdown("<h2 style='color:#002b5c;'>📊 Analyse Descriptive des Données</h2>", unsafe_allow_html=True)
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée disponible pour l'analyse.")
    else:
        # Métriques clés
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Audits", len(df))
        m2.metric("Attente Moyenne", f"{round(df['temps_urgence'].mean(), 1)} min")
        
        rdv_fav = (len(df[df['rdv_medecin_ligne'] == "Oui, ce serait préférable"]) / len(df)) * 100
        m3.metric("% Favorable RDV en ligne", f"{round(rdv_fav, 1)}%")

        st.divider()

        # Graphiques
        g1, g2 = st.columns(2)
        with g1:
            fig1 = px.pie(df, names='rdv_medecin_ligne', title="Préférence Prise de RDV en ligne", color_discrete_sequence=['#002b5c', '#66a3ff'])
            st.plotly_chart(fig1, use_container_width=True)
        with g2:
            avg_wait = df.groupby('nom_hopital')['temps_urgence'].mean().reset_index()
            fig2 = px.bar(avg_wait, x='nom_hopital', y='temps_urgence', title="Temps moyen d'attente par Hôpital", color_discrete_sequence=['#002b5c'])
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📜 Historique des Audits")
        st.dataframe(df, use_container_width=True)

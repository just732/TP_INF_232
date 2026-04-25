import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Portail National de Santé - Audit Centralisé", layout="wide")

# --- DESIGN PROFESSIONNEL (STYLE LANDING PAGE) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* Bannière d'accueil */
    .hero-banner {
        background: linear-gradient(rgba(0, 43, 92, 0.8), rgba(0, 43, 92, 0.8)), 
                    url('https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&q=80&w=2000');
        background-size: cover;
        background-position: center;
        padding: 80px 40px;
        color: white;
        text-align: center;
        border-radius: 0 0 40px 40px;
        margin-bottom: 30px;
    }
    .hero-banner h1 { font-size: 50px !important; font-weight: 700; }
    
    /* Style des Onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f1f4f8;
        padding: 10px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: white;
        border-radius: 10px;
        color: #002b5c;
        font-weight: bold;
    }
    
    /* Bulles d'information */
    .info-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #002b5c;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Formulaire */
    .stForm {
        background-color: #f8f9fa !important;
        border-radius: 20px !important;
        padding: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_sante_national.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, domicile TEXT, metier TEXT, raison_visite TEXT,
                    nom_hopital TEXT, temps_urgence INTEGER, attitude_globale TEXT,
                    eval_infirmieres TEXT, justif_infirmieres TEXT,
                    eval_medecins TEXT, justif_medecins TEXT,
                    rdv_ligne TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- HEADER ET OBJECTIF ---
st.markdown("""
    <div class="hero-banner">
        <h1>PORTAIL NATIONAL DE LA SANTÉ PUBLIQUE</h1>
        <p>Audit institutionnel et analyse quantitative de la performance hospitalière</p>
    </div>
    """, unsafe_allow_html=True)

# --- SECTION 1 : INFORMATIONS ET SERVICES (ONGLETS) ---
st.header("I. Informations Sanitaires et Présentation des Services")

tab_oms, tab_urgences, tab_specialite, tab_maternite = st.tabs([
    "🌍 Directives & Réformes (OMS)", 
    "🚑 Service des Urgences", 
    "🩺 Consultations Spécialisées", 
    "👶 Maternité & Pédiatrie"
])

with tab_oms:
    st.markdown("""
        <div class="info-card">
            <h4>Règles Essentielles de l'OMS</h4>
            <p>L'Organisation Mondiale de la Santé préconise une couverture santé universelle (CSU) basée sur la transparence des données et l'accès équitable aux soins de qualité. 
            Les réformes nationales actuelles visent la modernisation des plateaux techniques et la digitalisation du parcours patient.</p>
        </div>
        """, unsafe_allow_html=True)

with tab_urgences:
    st.markdown("""
        <div class="info-card">
            <h4>Prise en charge des Urgences</h4>
            <p>Service opérationnel 24h/24 et 7j/7. Notre audit mesure spécifiquement le temps de réaction entre l'arrivée du patient et sa première consultation par un interne ou un médecin spécialiste.</p>
        </div>
        """, unsafe_allow_html=True)

with tab_specialite:
    st.markdown("""
        <div class="info-card">
            <h4>Médecine Spécialisée</h4>
            <p>Services de Cardiologie, Neurologie, Chirurgie et Médecine Interne. Les rendez-vous sont gérés selon la priorité clinique et la disponibilité des praticiens de référence.</p>
        </div>
        """, unsafe_allow_html=True)

with tab_maternite:
    st.markdown("""
        <div class="info-card">
            <h4>Santé de la Mère et de l'Enfant</h4>
            <p>Programmes de vaccination, suivis prénataux et néonatals conformes aux protocoles internationaux de sécurité sanitaire.</p>
        </div>
        """, unsafe_allow_html=True)

# --- SECTION 2 : FORMULAIRE D'AUDIT CENTRALISÉ ---
st.markdown("---")
st.header("II. Collecte des Données d'Audit")

with st.form("form_audit_national"):
    st.subheader("1. Identification et Profil de l'Usager")
    c1, c2 = st.columns(2)
    nom = c1.text_input("Nom de famille")
    prenom = c2.text_input("Prénom")
    domicile = c1.text_input("Lieu de résidence")
    metier = c2.text_input("Profession")
    raison = st.text_area("Motif médical de la consultation (Description des symptômes)")

    st.subheader("2. Évaluation de l'Établissement")
    # C'est ici que l'utilisateur choisit son hôpital
    liste_hopitaux = ["Hôpital Général", "CHU Central", "Hôpital de District", "Clinique Conventionnée"]
    hopital_choisi = st.selectbox("Dans quel établissement avez-vous reçu des soins ?", liste_hopitaux)
    
    t_attente = st.slider("Temps d'attente estimé aux urgences (en minutes)", 0, 300, 30)
    attitude_g = st.selectbox("Attitude générale du personnel d'accueil", ["Insuffisante", "Moyenne", "Satisfaisante", "Excellente"])

    st.subheader("3. Audit Spécifique du Personnel")
    col_inf, col_med = st.columns(2)
    with col_inf:
        st.markdown("**Personnel Infirmier**")
        e_inf = st.select_slider("Qualité technique (Infirmiers)", options=["1", "2", "3", "4", "5"], key="inf")
        j_inf = st.text_area("Justification de la note (Infirmiers)")
    with col_med:
        st.markdown("**Corps Médical**")
        e_med = st.select_slider("Expertise et écoute (Médecins)", options=["1", "2", "3", "4", "5"], key="med")
        j_med = st.text_area("Justification de la note (Médecins)")

    st.subheader("4. Perspectives et Améliorations")
    rdv_ligne = st.radio("Souhaitez-vous la mise en place d'un système de rendez-vous en ligne avec un médecin spécifique ?", ["Favorable", "Défavorable"])
    suggestions = st.text_area("Quelles mesures concrètes préconisez-vous pour améliorer la qualité du service dans cet établissement ?")

    if st.form_submit_button("VALIDER ET TRANSMETTRE LE RAPPORT"):
        if nom and prenom and suggestions:
            conn = get_connection()
            c = conn.cursor()
            c.execute('''INSERT INTO rapports (nom, prenom, domicile, metier, raison_visite, 
                        nom_hopital, temps_urgence, attitude_globale, eval_infirmieres, 
                        justif_infirmieres, eval_medecins, justif_medecins, rdv_ligne, 
                        suggestions, date_soumission) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                     (nom, prenom, domicile, metier, raison, hopital_choisi, t_attente, 
                      attitude_g, e_inf, j_inf, e_med, j_med, rdv_ligne, suggestions, datetime.now()))
            conn.commit()
            conn.close()
            st.success("Rapport d'audit transmis avec succès aux autorités sanitaires.")
        else:
            st.error("Erreur : Les champs d'identification et les recommandations sont obligatoires.")

# --- SECTION 3 : ANALYSE DESCRIPTIVE ---
st.markdown("---")
st.header("III. Analyse Descriptive du Système de Santé")

conn = get_connection()
df = pd.read_sql_query("SELECT * FROM rapports", conn)
conn.close()

if df.empty:
    st.info("Aucune donnée disponible pour l'analyse statistique.")
else:
    # Indicateurs clés
    m1, m2, m3 = st.columns(3)
    m1.metric("Volume total d'Audits", len(df))
    m2.metric("Attente Moyenne", f"{round(df['temps_urgence'].mean(), 1)} min")
    taux = (len(df[df['rdv_ligne'] == "Favorable"]) / len(df)) * 100
    m3.metric("Adhésion au Digital", f"{round(taux, 1)}%")

    # Graphique de comparaison par hôpital
    st.subheader("Performance Temporelle par Établissement")
    fig = px.bar(df.groupby('nom_hopital')['temps_urgence'].mean().reset_index(), 
                 x='nom_hopital', y='temps_urgence', 
                 title="Moyenne des temps d'attente aux urgences par site",
                 color_discrete_sequence=['#002b5c'])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Préconisations d'amélioration des usagers")
    st.dataframe(df[['nom_hopital', 'nom', 'suggestions', 'date_soumission']], use_container_width=True)

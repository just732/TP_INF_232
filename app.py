import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DU THÈME (BLEU NUIT) ---
st.set_page_config(page_title="Audit Qualité Hospitalière", layout="wide")

# Injection CSS pour un thème Bleu Nuit élégant
st.markdown("""
    <style>
    .main {
        background-color: #1a2634;
        color: #ffffff;
    }
    .stApp {
        background-color: #1a2634;
    }
    .sidebar .sidebar-content {
        background-color: #111b27;
    }
    h1, h2, h3, p {
        color: #e0e6ed !important;
    }
    .stButton>button {
        background-color: #2c5282;
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #2d3748 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_stdio=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_hopital.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, domicile TEXT, metier TEXT,
                    raison_visite TEXT, nom_hopital TEXT, temps_urgence INTEGER,
                    qualite_soins TEXT, attitude_personnel TEXT, efficacite_travail TEXT,
                    option_rdv TEXT, date_enregistrement DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- NAVIGATION ---
st.sidebar.title("🩺 Navigation")
page = st.sidebar.radio("Aller vers :", ["🏠 Accueil", "📝 Formulaire d'Audit", "📊 Analyse des Données"])

# --- PAGE 1 : ACCUEIL (PAGE DE GARDE) ---
if page == "🏠 Accueil":
    st.title("Audit National pour l'Amélioration des Services Hospitaliers")
    st.image("https://img.freepik.com/vecteurs-libre/fond-bleu-abstrait-forme-vague_343694-2330.jpg?size=626&ext=jpg", use_container_width=True)
    
    st.markdown("""
    ### 📌 À propos de cet Audit
    Cette application a été conçue pour recueillir des données précises sur l'expérience des patients dans nos établissements hospitaliers.
    
    **L'objectif est double :**
    1. **Identifier les points faibles** dans la prise en charge des urgences et l'attitude du personnel.
    2. **Moderniser les services** en évaluant la demande pour la digitalisation des prises de rendez-vous.
    
    *Vos réponses sont précieuses et permettront d'orienter les futures réformes de santé publique.*
    
    ---
    **Instructions :**
    - Cliquez sur l'onglet **Formulaire d'Audit** dans la barre latérale pour commencer.
    - Vos données seront analysées anonymement dans l'onglet **Analyse**.
    """)

# --- PAGE 2 : FORMULAIRE D'AUDIT ---
elif page == "📝 Formulaire d'Audit":
    st.header("Saisie des informations de l'audit")
    
    with st.form("audit_form", clear_on_submit=True):
        st.subheader("👤 Identification du Patient")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom")
        prenom = c2.text_input("Prénom")
        domicile = c1.text_input("Ville / Quartier de domicile")
        metier = c2.text_input("Profession")
        
        st.subheader("🏥 Contexte de la visite")
        raison_visite = st.text_area("De quoi souffriez-vous ? (Raison de votre présence à l'hôpital)")
        nom_h = st.selectbox("Hôpital concerné", ["Hôpital Central", "Clinique Sainte-Marie", "CHU Nord", "Hôpital de District"])
        
        st.subheader("📋 Évaluation du service")
        col_a, col_b = st.columns(2)
        with col_a:
            t_urgence = st.slider("Temps d'attente aux urgences (min)", 0, 180, 20)
            qualite = st.select_slider("Qualité des soins", options=["Médiocre", "Passable", "Satisfaisant", "Excellent"])
        with col_b:
            attitude = st.selectbox("Attitude du personnel", ["Impoli", "Indifférent", "Professionnel", "Chaleureux"])
            travail = st.radio("Façon de travailler", ["Désorganisée", "Lente", "Efficace"])
            rdv_en_ligne = st.radio("L'option de RDV en ligne est-elle préférable ?", ["Oui", "Non"])

        submitted = st.form_submit_button("Envoyer l'Audit")
        
        if submitted:
            if nom and prenom:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, domicile, metier, raison_visite, 
                            nom_hopital, temps_urgence, qualite_soins, attitude_personnel, 
                            efficacite_travail, option_rdv, date_enregistrement) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, domicile, metier, raison_visite, nom_h, t_urgence, 
                          qualite, attitude, travail, rdv_en_ligne, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ Merci ! Vos données ont été transmises à la base de l'audit.")
            else:
                st.warning("⚠️ Veuillez remplir au moins le nom et le prénom.")

# --- PAGE 3 : ANALYSE DES DONNÉES ---
elif page == "📊 Analyse des Données":
    st.header("Statistiques Descriptives de l'Audit")
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("En attente de données pour générer les graphiques...")
    else:
        # Métriques
        m1, m2, m3 = st.columns(3)
        m1.metric("Total des Audits", len(df))
        m2.metric("Moyenne Urgences", f"{round(df['temps_urgence'].mean(), 1)} min")
        rdv_taux = (len(df[df['option_rdv'] == "Oui"]) / len(df)) * 100
        m3.metric("Favorable RDV en ligne", f"{round(rdv_taux, 1)}%")

        st.divider()

        # Graphiques avec couleurs adaptées au thème nuit
        g1, g2 = st.columns(2)
        with g1:
            st.subheader("Répartition de l'attitude du personnel")
            fig1 = px.pie(df, names='attitude_personnel', hole=0.4, template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
            
        with g2:
            st.subheader("Temps d'attente moyen par établissement")
            avg_h = df.groupby('nom_hopital')['temps_urgence'].mean().reset_index()
            fig2 = px.bar(avg_h, x='nom_hopital', y='temps_urgence', template="plotly_dark", color='nom_hopital')
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Détails des répondants")
        st.dataframe(df[['nom', 'prenom', 'domicile', 'metier', 'raison_visite', 'date_enregistrement']], use_container_width=True)

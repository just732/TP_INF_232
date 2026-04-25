import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Audit Médical Pro", layout="wide")

# --- DESIGN STYLE "BULLE" MODERNE ---
st.markdown("""
    <style>
    /* Fond dégradé bleu professionnel */
    .stApp {
        background: linear-gradient(180deg, #004a99 0%, #f0f4f8 40%);
        color: #1E1E1E;
    }
    
    /* Grande Bulle d'Objectif (Police augmentée) */
    .objective-bubble {
        background-color: white;
        padding: 40px;
        border-radius: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-left: 15px solid #002b5c;
        text-align: center;
    }
    .objective-bubble h1 {
        font-size: 50px !important;
        color: #002b5c !important;
        font-weight: 800;
        margin-bottom: 15px;
    }
    .objective-bubble p {
        font-size: 24px !important;
        color: #333;
        line-height: 1.5;
    }

    /* Cartes de méthode */
    .method-card {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 5px solid #0056b3;
    }

    /* Lisibilité du formulaire (Texte noir sur fond blanc) */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: white !important;
        color: black !important;
        border-radius: 10px !important;
    }
    label { 
        font-size: 19px !important; 
        font-weight: bold !important; 
        color: #002b5c !important; 
    }
    
    /* Bouton d'action */
    .stButton>button {
        background-color: #002b5c;
        color: white;
        border-radius: 50px;
        padding: 15px 40px;
        font-size: 22px;
        font-weight: bold;
        width: 100%;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_final_hopital.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, domicile TEXT, metier TEXT,
                    raison_visite TEXT, nom_hopital TEXT, temps_urgence INTEGER,
                    attitude_globale TEXT, organisation_travail TEXT,
                    eval_infirmieres TEXT, justif_infirmieres TEXT,
                    eval_medecins TEXT, justif_medecins TEXT,
                    rdv_medecin_ligne TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- NAVIGATION ---
st.sidebar.title("🏨 NAVIGATION")
page = st.sidebar.radio("Menu", ["🏠 Accueil", "📝 Formulaire d'Audit", "📊 Dashboard Analyse"])

# --- PAGE 1 : ACCUEIL ---
if page == "🏠 Accueil":
    st.markdown("""
        <div class="objective-bubble">
            <h1>OBJECTIF DE L'AUDIT</h1>
            <p>Améliorer la qualité des services hospitaliers en analysant le parcours patient, l'efficacité du personnel et la pertinence de la digitalisation des soins.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="method-card"><h3>📈 Analyse</h3><p>Méthodes quantitatives de mesure.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="method-card"><h3>🤝 Personnel</h3><p>Évaluation globale et spécifique.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="method-card"><h3>🚀 Futur</h3><p>Digitalisation des rendez-vous.</p></div>', unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE ---
elif page == "📝 Formulaire d'Audit":
    st.markdown("<h1 style='color:white; text-align:center;'>📝 Questionnaire d'Audit</h1>", unsafe_allow_html=True)
    
    with st.form("audit_form", clear_on_submit=True):
        st.subheader("👤 1. Identification & Contexte")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom")
        prenom = c2.text_input("Prénom")
        dom = c1.text_input("Domicile")
        job = c2.text_input("Métier")
        raison = st.text_area("Raison de votre visite (Symptômes / Souffrances)")
        
        st.subheader("🏥 2. Évaluation Globale")
        hopital = st.selectbox("Hôpital concerné", ["Hôpital Général", "CHU Central", "Clinique Privée"])
        t_urgence = st.slider("Temps d'attente urgences (min)", 0, 180, 20)
        attitude_g = st.selectbox("Attitude globale du personnel", ["Médiocre", "Neutre", "Accueillante", "Excellente"])
        travail_g = st.radio("Organisation générale du travail", ["Désorganisée", "Passable", "Très organisée"])

        st.subheader("👩‍ 3. Détail Personnel Infirmier")
        e_inf = st.select_slider("Note pour les Infirmières", options=["Basse", "Moyenne", "Haute", "Parfaite"])
        j_inf = st.text_area("Justification (Infirmières)")

        st.subheader("👨‍⚕️ 4. Détail Corps Médical (Médecins)")
        e_med = st.select_slider("Note pour les Médecins", options=["Basse", "Moyenne", "Haute", "Parfaite"])
        j_med = st.text_area("Justification (Médecins)")

        st.subheader("🌐 5. Digitalisation")
        rdv = st.radio("Prendre rendez-vous en ligne avec un médecin spécifique de cet hôpital vous conviendrait-il ?", 
                      ["Oui, ce serait idéal", "Non, je ne préfère pas"])

        if st.form_submit_button("SOUMETTRE L'AUDIT"):
            if nom and prenom and raison:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, domicile, metier, raison_visite, 
                            nom_hopital, temps_urgence, attitude_globale, organisation_travail,
                            eval_infirmieres, justif_infirmieres, eval_medecins, justif_medecins, 
                            rdv_medecin_ligne, date_soumission) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, dom, job, raison, hopital, t_urgence, attitude_g, travail_g,
                          e_inf, j_inf, e_med, j_med, rdv, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ Audit enregistré avec succès !")
                st.balloons()
            else:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires.")

# --- PAGE 3 : ANALYSE ---
elif page == "📊 Dashboard Analyse":
    st.markdown("<h1 style='color:white; text-align:center;'>📊 Analyse Descriptive</h1>", unsafe_allow_html=True)
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("En attente de données...")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Audits", len(df))
        c2.metric("Attente Moy.", f"{round(df['temps_urgence'].mean(), 1)} min")
        rdv_p = (len(df[df['rdv_medecin_ligne'].str.contains("Oui")]) / len(df)) * 100
        c3.metric("Favorable RDV Ligne", f"{round(rdv_p, 1)}%")

        st.divider()

        g1, g2 = st.columns(2)
        with g1:
            fig1 = px.pie(df, names='attitude_globale', title="Attitude Globale du Personnel", hole=0.3)
            st.plotly_chart(fig1, use_container_width=True)
        with g2:
            fig2 = px.bar(df, x='nom_hopital', y='temps_urgence', title="Temps moyen d'urgence")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📋 Justifications détaillées")
        st.dataframe(df[['nom', 'justif_infirmieres', 'justif_medecins', 'rdv_medecin_ligne']], use_container_width=True)

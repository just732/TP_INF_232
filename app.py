import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide")

# --- DESIGN "PATIENT PLUS" ---
st.markdown("""
    <style>
    /* Image de fond principale : Hôpital Général */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.75), rgba(0, 43, 92, 0.75)), 
                    url('https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg/1200px-H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* Bulles d'information avec images */
    .bubble {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px; padding: 20px; color: #1a1a1a; margin-bottom: 20px;
        border-top: 6px solid #e1395f; min-height: 350px;
    }
    .bubble img { width: 100%; border-radius: 10px; margin-bottom: 10px; height: 180px; object-fit: cover; }
    
    /* Bouton rouge Patient Plus */
    .stButton>button {
        background-color: #e1395f !important; color: white !important;
        border-radius: 50px !important; padding: 15px !important;
        width: 100%; font-weight: bold !important; border: none !important;
    }
    
    /* Style Admin */
    .admin-box { background-color: #f1f4f8; padding: 20px; border-radius: 15px; color: #1a1a1a; }
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

# --- BARRE LATÉRALE (Navigation) ---
st.sidebar.title("🏥 Patient Plus")
role = st.sidebar.radio("Accès :", ["Patient (Public)", "Enquêteur (Admin)"])

# --- ESPACE PATIENT (PUBLIC) ---
if role == "Patient (Public)":
    menu = st.sidebar.selectbox("Aller vers :", ["Accueil", "Remplir l'Audit"])

    if menu == "Accueil":
        st.markdown("<h1 style='text-align:center;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:20px;'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="bubble">
                    <img src="https://www.social-sante.gouv.fr/IMG/jpg/pediatrie_hopital.jpg">
                    <h4>Hôpitaux et Surcharge</h4>
                    <p><b>Hôpitaux Régionaux :</b> 4 000 à 6 000 hospitalisations/an.</p>
                    <p><b>Performance :</b> Seuls 48% des 172 hôpitaux publics sont jugés performants.</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="bubble">
                    <img src="https://www.unicef.org/cameroon/sites/unicef.org.cameroon/files/styles/hero_desktop/public/UNI354546.jpg">
                    <h4>Maternité au Cameroun</h4>
                    <p><b>Admission :</b> 35,9% des accouchements se font encore à domicile sans assistance médicale.</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.write("---")
        if st.button("📝 COMMENCER L'AUDIT MAINTENANT"):
            st.info("Utilisez le menu à gauche pour sélectionner 'Remplir l'Audit'.")

    elif menu == "Remplir l'Audit":
        st.markdown("<h2>📝 Formulaire d'Audit Patient</h2>", unsafe_allow_html=True)
        with st.form("audit_form"):
            st.subheader("1. Identification")
            c1, c2 = st.columns(2)
            nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
            age, sexe = c1.number_input("Âge", 0, 110, 25), c2.selectbox("Sexe", ["Masculin", "Féminin"])
            metier, email = c1.text_input("Métier"), c2.text_input("Email")
            dob, dom = c1.date_input("Date de naissance"), c2.text_input("Lieu de résidence")

            st.subheader("2. Détails du séjour")
            hopital = st.selectbox("Hôpital", ["Hôpital Général", "Hôpital Central", "Hôpital de Laquintinie", "CHU"])
            service, maladie = st.text_input("Service (ex: Urgences)"), st.text_input("Motif/Maladie")
            
            st.subheader("3. Évaluation")
            attente = st.slider("Attente (min)", 0, 300, 30)
            c_inf, c_med = st.columns(2)
            e_inf = c_inf.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
            j_inf = c_inf.text_area("Justification Infirmières")
            e_med = c_med.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
            j_med = c_med.text_area("Justification Médecins")

            st.subheader("4. Suggestions")
            sug = st.text_area("Comment améliorer le service selon vous ?")
            rdv = st.radio("Favorable au RDV en ligne ?", ["Oui", "Non"])

            if st.form_submit_button("VALIDER L'AUDIT"):
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, domicile, email,
                            maladie, service, hopital, attente, eval_inf, justif_inf, eval_med, justif_med,
                            rdv_ligne, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                         (nom, prenom, age, sexe, metier, str(dob), dom, email, maladie, service, hopital, attente, e_inf, j_inf, e_med, j_med, rdv, sug, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ Envoyé ! Vos réponses ont été transmises à l'enquêteur.")

# --- ESPACE ENQUÊTEUR (ADMIN) ---
elif role == "Enquêteur (Admin)":
    st.markdown("<h2>🔐 Espace Enquêteur</h2>", unsafe_allow_html=True)
    password = st.text_input("Entrez le mot de passe pour voir les résultats :", type="password")
    
    if password == "admin123": # Vous pouvez changer ce mot de passe
        st.success("Accès autorisé.")
        
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM rapports", conn)
        conn.close()

        if df.empty:
            st.warning("Aucune donnée collectée pour le moment.")
        else:
            st.markdown("### 📊 Analyse Descriptive Automatique")
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Audits", len(df))
            m2.metric("Attente Moyenne", f"{round(df['attente'].mean(), 1)} min")
            fav = (len(df[df['rdv_ligne'] == "Oui"]) / len(df)) * 100
            m3.metric("% RDV en ligne", f"{round(fav, 1)}%")

            st.plotly_chart(px.bar(df, x="hopital", y="attente", color="attitude_g", title="Performance par Hôpital"))
            
            st.markdown("### 📋 Réponses détaillées (Tableau)")
            st.dataframe(df)
    elif password != "":
        st.error("Mot de passe incorrect.")

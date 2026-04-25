import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Audit Médical Pro", layout="wide")

# --- DESIGN STYLE "BULLE" (Inspiré de l'image de voyage) ---
st.markdown("""
    <style>
    /* Fond dégradé bleu */
    .stApp {
        background: linear-gradient(180deg, #0056b3 0%, #f0f2f6 30%);
        color: #1E1E1E;
    }
    
    /* Grande Bulle d'Objectif */
    .objective-bubble {
        background-color: white;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin: 20px 0;
        border-left: 10px solid #002b5c;
    }
    .objective-bubble h1 {
        font-size: 45px !important;
        color: #002b5c !important;
        margin-bottom: 10px;
    }
    .objective-bubble p {
        font-size: 22px !important;
        color: #444;
        line-height: 1.4;
    }

    /* Petites Bulles de Méthode */
    .method-card {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 5px solid #0056b3;
    }
    .method-card h3 { font-size: 28px; color: #0056b3; }

    /* Style du Formulaire */
    .stTextInput, .stTextArea, .stSelectbox {
        background-color: white !important;
        border-radius: 15px !important;
    }
    label { 
        font-size: 18px !important; 
        font-weight: bold !important; 
        color: #002b5c !important; 
    }
    
    /* Bouton type Mobile */
    .stButton>button {
        background-color: #002b5c;
        color: white;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 20px;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES (Mise à jour avec Justifications) ---
def get_connection():
    return sqlite3.connect('audit_hospitalier_v4.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, domicile TEXT, metier TEXT,
                    raison_visite TEXT, nom_hopital TEXT, temps_urgence INTEGER,
                    eval_infirmieres TEXT, justif_infirmieres TEXT,
                    eval_medecins TEXT, justif_medecins TEXT,
                    rdv_medecin_ligne TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- BARRE LATÉRALE ---
st.sidebar.title("🏨 MENU AUDIT")
page = st.sidebar.radio("Navigation", ["🏠 Accueil", "📝 Faire l'Audit", "📊 Statistiques"])

# --- PAGE 1 : ACCUEIL ---
if page == "🏠 Accueil":
    # Bulle d'objectif GÉANTE
    st.markdown("""
        <div class="objective-bubble">
            <h1>OBJECTIF DE L'AUDIT</h1>
            <p>Améliorer radicalement la qualité des soins en transformant chaque témoignage patient en levier de réforme pour nos hôpitaux nationaux.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="method-card"><h3>🧑‍⚕️ Personnel</h3><p>Évaluation rigoureuse des soignants.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="method-card"><h3>⏳ Temps</h3><p>Analyse des délais aux urgences.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="method-card"><h3>💻 Digital</h3><p>Vers les rendez-vous en ligne.</p></div>', unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE D'AUDIT ---
elif page == "📝 Faire l'Audit":
    st.markdown("<h1 style='color:white;'>📝 Questionnaire d'Audit</h1>", unsafe_allow_html=True)
    
    with st.form("audit_form", clear_on_submit=True):
        # Section Patient
        st.markdown("### 👤 Votre Profil")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom de famille")
        prenom = c2.text_input("Prénom")
        dom = c1.text_input("Domicile")
        job = c2.text_input("Métier")
        
        # Section Contexte
        st.markdown("### 🏥 Contexte de Visite")
        raison = st.text_area("De quoi souffriez-vous ? (Justification médicale)")
        hopital = st.selectbox("Hôpital concerné", ["Hôpital Général", "CHU Central", "Clinique de l'Espoir", "Hôpital de District"])
        t_urgence = st.slider("Temps d'attente urgences (min)", 0, 180, 15)

        # SECTION INFIRMIÈRES (Évaluation + Justification)
        st.markdown("### 👩‍ Personnels Infirmiers")
        e_inf = st.select_slider("Note pour les Infirmières", options=["Désagréables", "Passables", "Professionnelles", "Excellentes"])
        j_inf = st.text_area("Justification (Infirmières) : Pourquoi cette note ?")

        # SECTION MÉDECINS (Évaluation + Justification)
        st.markdown("### 👨‍⚕️ Médecins")
        e_med = st.select_slider("Note pour les Médecins", options=["Médiocres", "Passables", "Compétents", "Excellents"])
        j_med = st.text_area("Justification (Médecins) : Détaillez votre expérience")

        # Section Digitalisation
        st.markdown("### 🌐 Futur Digital")
        rdv = st.radio("Prendre rendez-vous en ligne avec un médecin spécifique vous conviendrait-il ?", 
                      ["Oui, c'est indispensable", "Non, je ne préfère pas"])

        if st.form_submit_button("SOUMETTRE L'AUDIT"):
            if nom and prenom and raison:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, domicile, metier, raison_visite, 
                            nom_hopital, temps_urgence, eval_infirmieres, justif_infirmieres, 
                            eval_medecins, justif_medecins, rdv_medecin_ligne, date_soumission) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, dom, job, raison, hopital, t_urgence, 
                          e_inf, j_inf, e_med, j_med, rdv, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ Audit envoyé avec succès !")
                st.balloons()
            else:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires.")

# --- PAGE 3 : STATISTIQUES ---
elif page == "📊 Statistiques":
    st.markdown("<h1 style='color:white;'>📊 Résultats de l'Audit</h1>", unsafe_allow_html=True)
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.warning("Aucune donnée disponible.")
    else:
        # KPI en Bulles
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Avis", len(df))
        c2.metric("Attente Moy.", f"{round(df['temps_urgence'].mean(), 1)} min")
        rdv_pos = (len(df[df['rdv_medecin_ligne'].str.contains("Oui")]) / len(df)) * 100
        c3.metric("% RDV En Ligne", f"{round(rdv_pos, 1)}%")

        st.divider()

        # Graphiques
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig1 = px.pie(df, names='eval_medecins', title="Satisfaction Médecins", hole=0.4)
            st.plotly_chart(fig1, use_container_width=True)
        with col_g2:
            fig2 = px.bar(df, x='nom_hopital', y='temps_urgence', color='eval_infirmieres', title="Temps d'attente par Hôpital")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📝 Détails et Justifications")
        st.dataframe(df[['nom', 'nom_hopital', 'justif_infirmieres', 'justif_medecins']], use_container_width=True)

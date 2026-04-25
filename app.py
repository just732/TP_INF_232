import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION DES VARIABLES ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'investigateur' not in st.session_state: st.session_state.investigateur = None

def changer_page(nom): st.session_state.page = nom

# --- DONNÉES NATIONALES ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU de Yaoundé", "Hôpital Gynéco-Obstétrique"],
    "Est": ["Hôpital Régional de Bertoua", "Hôpital de District de Batouri"],
    "Extrême-Nord": ["Hôpital Régional de Maroua", "Hôpital de District de Mokolo"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie", "Hôpital de District de Bonassama"],
    "Nord": ["Hôpital Régional de Garoua", "Hôpital de District de Guider"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda", "Hôpital de District de Wum"],
    "Ouest": ["Hôpital Régional de Bafoussam", "Hôpital de District de Dschang"],
    "Sud": ["Hôpital Régional d'Ebolowa", "Hôpital de District de Kribi"],
    "Sud-Ouest": ["Hôpital Régional de Buea", "Hôpital Régional de Limbe"]
}

# --- DESIGN PROFESSIONNEL (CSS) ---
st.markdown("""
    <style>
    /* Image de fond de l'Hôpital Général */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.8), rgba(0, 43, 92, 0.8)), 
                    url('https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* Bulles d'info en haut */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 20px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 10px solid #e1395f;
    }

    /* Style des cartes de navigation (Bulles cliquables) */
    .stButton>button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 20px !important;
        height: 150px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        transition: 0.3s !important;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #e1395f !important;
        border-color: #e1395f !important;
        transform: translateY(-5px);
    }

    /* Boites blanches pour formulaires */
    .white-container {
        background-color: white; padding: 30px; border-radius: 20px; color: #1a1a1a;
    }
    label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('audit_national_v9.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, email TEXT, region TEXT, hopital TEXT, 
                    motif TEXT, attente INTEGER, eval_inf TEXT, justif_inf TEXT, 
                    eval_med TEXT, justif_med TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:22px;'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>", unsafe_allow_html=True)

    # 1. Dashboard d'Analyse (Calculé automatiquement)
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        st.markdown("### Analyse Descriptive Globale")
        c1, c2, c3 = st.columns(3)
        c1.metric("Audits Complétés", len(df))
        c2.metric("Moyenne Attente", f"{round(df['attente'].mean(), 1)} min")
        c3.metric("Régions Audités", df['region'].nunique())
        
        # Graphique résumé
        fig = px.bar(df.groupby('region').size().reset_index(name='Nombre'), x='region', y='Nombre', template="plotly_dark", title="Répartition des audits par région")
        st.plotly_chart(fig, use_container_width=True)

    # 2. Bulles d'informations terrain
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="info-card"><h4>Hôpitaux Publics</h4><p>Le Cameroun compte 172 hôpitaux publics. Seuls 48% remplissent les critères de performance.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="info-card"><h4>Services Maternité</h4><p>35,9% des accouchements se font hors milieu médical, impactant la sécurité sanitaire.</p></div>', unsafe_allow_html=True)

    # 3. Navigation par Bulles (Boutons stylisés en Cartes)
    st.markdown("<h2 style='text-align:center;'>Naviguer dans l'application</h2>", unsafe_allow_html=True)
    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        st.button("📝 AUDIT PATIENT", on_click=lambda: changer_page("Audit"))
    with nav2:
        st.button("🔐 ESPACE ADMIN", on_click=lambda: changer_page("Admin"))
    with nav3:
        st.button("ℹ️ INFORMATIONS", on_click=lambda: changer_page("Infos"))

# --- PAGE 2 : AUDIT PATIENT ---
elif st.session_state.page == "Audit":
    st.button("⬅ Retour", on_click=lambda: changer_page("Accueil"))
    st.header("Formulaire d'Audit National")
    
    if st.session_state.investigateur:
        st.info(f"Audit supervisé par l'enquêteur : {st.session_state.investigateur['nom']}")

    with st.form("audit_form"):
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom de famille")
        prenom = c2.text_input("Prénom")
        age = c1.number_input("Âge", 0, 110, 25)
        email = c2.text_input("Email de contact")
        
        reg = st.selectbox("Région de résidence", list(data_cameroun.keys()))
        hop = st.selectbox("Hôpital audité", data_cameroun[reg])
        motif = st.text_area("Motif de la consultation (Souffrances constatées)")
        
        attente = st.slider("Temps d'attente aux urgences (min)", 0, 300, 30)
        
        ci, cm = st.columns(2)
        e_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
        j_inf = ci.text_area("Justification (Infirmières)")
        e_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
        j_med = cm.text_area("Justification (Médecins)")
        
        sug = st.text_area("Quelles mesures concrètes préconisez-vous pour améliorer le service ?")

        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = get_connection()
            c = conn.cursor()
            c.execute('''INSERT INTO rapports (nom, prenom, age, email, region, hopital, motif, attente, 
                        eval_inf, justif_inf, eval_med, justif_med, suggestions, date_soumission) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                     (nom, prenom, age, email, reg, hop, motif, attente, e_inf, j_inf, e_med, j_med, sug, datetime.now()))
            conn.commit()
            conn.close()
            st.success("Données envoyées. Merci de votre contribution.")
            changer_page("Accueil")

# --- PAGE 3 : ESPACE ENQUÊTEUR ---
elif st.session_state.page == "Admin":
    st.button("⬅ Retour", on_click=lambda: changer_page("Accueil"))
    
    tab_compte, tab_resultats = st.tabs(["👤 Créer un compte", "📊 Résultats de l'Audit"])
    
    with tab_compte:
        st.markdown("<div class='white-container'>", unsafe_allow_html=True)
        st.subheader("Identification de l'Enquêteur")
        with st.form("admin_account"):
            nom_e = st.text_input("Nom complet de l'enquêteur")
            email_e = st.text_input("Adresse Email professionnelle")
            job_e = st.text_input("Poste / Institution")
            if st.form_submit_button("CRÉER MON PROFIL ENQUÊTEUR"):
                st.session_state.investigateur = {"nom": nom_e, "email": email_e}
                st.success("Compte Enquêteur activé pour cet audit.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_resultats:
        pwd = st.text_input("Mot de passe de sécurité", type="password")
        if pwd == "admin123":
            conn = get_connection()
            df = pd.read_sql_query("SELECT * FROM rapports", conn)
            conn.close()
            st.write(df)
            st.download_button("Télécharger les données (CSV)", df.to_csv(), "audit_extract.csv")

# --- PAGE 4 : INFOS ---
elif st.session_state.page == "Infos":
    st.button("⬅ Retour", on_click=lambda: changer_page("Accueil"))
    st.markdown("<div class='white-container'><h3>À propos de Patient Plus</h3><p>Ce système centralise les avis des citoyens pour orienter les réformes du système de santé au Cameroun.</p></div>", unsafe_allow_html=True)

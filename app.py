import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'admin_auth' not in st.session_state: st.session_state.admin_auth = False
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

# --- DESIGN CSS (RETOUR AUX GRANDES TAILLES) ---
st.markdown("""
    <style>
    /* Image de fond Hôpital Général */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.85), rgba(0, 43, 92, 0.85)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* LES GRANDES BULLES (Comme avant, mais sans bouton rouge) */
    .nav-bubble .stButton > button {
        height: 350px !important;  /* Taille géante */
        width: 100% !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 3px solid white !important;
        border-radius: 35px !important;
        font-size: 35px !important;
        font-weight: bold !important;
        transition: 0.4s !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .nav-bubble .stButton > button:hover {
        background-color: #e1395f !important;
        border-color: #e1395f !important;
        transform: translateY(-15px) scale(1.02) !important;
    }

    /* LE PETIT BOUTON RETOUR RECTANGULAIRE */
    .back-btn-box .stButton > button {
        height: 35px !important;
        width: 120px !important;
        font-size: 13px !important;
        font-weight: bold !important;
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid white !important;
        border-radius: 5px !important;
        margin-bottom: 20px !important;
    }

    /* Cartes d'info */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 20px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 10px solid #e1395f;
    }
    .white-box { background-color: white; padding: 30px; border-radius: 20px; color: #1a1a1a; }
    label { color: white !important; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('audit_v12_final.db', check_same_thread=False)
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
    st.markdown("<h1 style='text-align:center; font-size:75px; margin-bottom:0;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:28px; opacity:0.9;'>Audit National de la Qualité des Services d'Urgence du Cameroun</p>", unsafe_allow_html=True)

    # Dashboard de synthèse (KPIs)
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Audits Enregistrés", len(df))
        c2.metric("Attente Moyenne", f"{round(df['attente'].mean(), 1)} min")
        c3.metric("Régions Couvertes", df['region'].nunique())

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="info-card"><h4>Performance Hospitalière</h4><p>Sur 172 hôpitaux publics, cet audit analyse les leviers pour dépasser le taux de performance actuel de 48%.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="info-card"><h4>Santé Maternelle</h4><p>35,9% des naissances hors milieu médical. Vos données aident à sécuriser les maternités institutionnelles.</p></div>', unsafe_allow_html=True)

    # LES GRANDES BULLES GÉANTES ET FLOTTANTES
    st.markdown("<br><br>", unsafe_allow_html=True)
    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        st.markdown('<div class="nav-bubble">', unsafe_allow_html=True)
        st.button("📝 AUDIT PATIENT", on_click=lambda: changer_page("Audit"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with nav2:
        st.markdown('<div class="nav-bubble">', unsafe_allow_html=True)
        st.button("🔐 ESPACE ADMIN", on_click=lambda: changer_page("Admin"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with nav3:
        st.markdown('<div class="nav-bubble">', unsafe_allow_html=True)
        st.button("ℹ️ INFOS PROJET", on_click=lambda: changer_page("Infos"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2 : AUDIT PATIENT ---
elif st.session_state.page == "Audit":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.header("Formulaire d'Audit National")
    with st.form("audit_form"):
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        email, age = c1.text_input("Email"), c2.number_input("Âge", 0, 110, 25)
        reg = st.selectbox("Région", list(data_cameroun.keys()))
        hop = st.selectbox("Établissement", data_cameroun[reg])
        motif = st.text_area("Motif de votre consultation (Souffrance)")
        attente = st.slider("Délai d'attente aux urgences (min)", 0, 300, 30)
        
        ci, cm = st.columns(2)
        e_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
        j_inf = ci.text_area("Justification (Infirmières)")
        e_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
        j_med = cm.text_area("Justification (Médecins)")
        sug = st.text_area("Mesures préconisées pour améliorer le service")

        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO rapports (nom, prenom, age, email, region, hopital, motif, attente, eval_inf, justif_inf, eval_med, justif_med, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                     (nom, prenom, age, email, reg, hop, motif, attente, e_inf, j_inf, e_med, j_med, sug, datetime.now()))
            conn.commit()
            conn.close()
            st.success("Audit transmis. Merci !")
            changer_page("Accueil")

# --- PAGE 3 : ESPACE ADMIN ---
elif st.session_state.page == "Admin":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)

    t1, t2 = st.tabs(["👤 Création Compte Enquêteur", "📊 Accès aux Résultats"])
    
    with t1:
        st.markdown("<div class='white-box'>", unsafe_allow_html=True)
        with st.form("creer_admin"):
            nom_e = st.text_input("Nom de l'enquêteur")
            email_e = st.text_input("Email professionnel")
            if st.form_submit_button("ENREGISTRER MON COMPTE"):
                st.session_state.investigateur = nom_e
                st.success("Compte Enquêteur créé.")
        st.markdown("</div>", unsafe_allow_html=True)

    with t2:
        pwd = st.text_input("Code de sécurité", type="password")
        if st.button("DÉVERROUILLER"):
            if pwd == "admin123":
                st.session_state.admin_auth = True
            else: st.error("Code erroné.")
            
        if st.session_state.admin_auth:
            conn = get_connection()
            df = pd.read_sql_query("SELECT * FROM rapports", conn)
            conn.close()
            st.markdown("<div class='white-box'>", unsafe_allow_html=True)
            st.write(df)
            st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 4 : INFOS ---
elif st.session_state.page == "Infos":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div class='white-box'><h3>Fonctionnement</h3><p>Patient Plus centralise les données nationales pour une analyse quantitative de l'offre de soins.</p></div>", unsafe_allow_html=True)

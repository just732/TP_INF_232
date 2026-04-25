import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- 2. INITIALISATION ET NAVIGATION ---
if 'page' not in st.session_state: 
    st.session_state.page = "Accueil"
if 'admin_auth' not in st.session_state: 
    st.session_state.admin_auth = False

def changer_page(nom): 
    st.session_state.page = nom
    st.rerun()

# --- 3. DONNÉES ET BASE DE DONNÉES ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU", "Gynéco-Obstétrique"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie", "Hôpital de Bonassama"],
    "Extrême-Nord": ["Hôpital Régional de Maroua", "Hôpital de Kousseri"],
    "Nord": ["Hôpital Régional de Garoua"], "Est": ["Hôpital Régional de Bertoua"],
    "Ouest": ["Hôpital Régional de Bafoussam"], "Sud": ["Hôpital Régional d'Ebolowa"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda"], "Sud-Ouest": ["Hôpital Régional de Buea"]
}

def get_connection(): return sqlite3.connect('patient_plus_final_national.db', check_same_thread=False)
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, email TEXT, region TEXT, hopital TEXT, 
                    motif TEXT, attente INTEGER, eval_inf TEXT, eval_med TEXT, 
                    suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()
init_db()

# --- 4. DESIGN CSS (BULLES STYLE IMAGE) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 30, 70, 0.8), rgba(0, 30, 70, 0.8)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* Style des bulles de navigation */
    .stButton button {
        width: 100%; height: 220px;
        background-color: transparent !important; color: transparent !important;
        border: none !important; position: absolute; z-index: 10; cursor: pointer;
    }
    .nav-card {
        background-color: #122a45; border: 2px solid white; border-radius: 15px;
        padding: 30px 10px; text-align: center; height: 220px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        transition: 0.3s;
    }
    .nav-card:hover { background-color: #1c3d63; transform: scale(1.02); }
    .card-icon { font-size: 45px; margin-bottom: 10px; }
    .card-title { font-size: 26px; font-weight: bold; color: white; text-transform: uppercase; }
    .card-subtitle { font-size: 15px; color: #cbd5e0; margin-top: 5px; }

    /* Cards d'info et formulaires */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 15px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 8px solid #e1395f;
    }
    .white-box { background: white; padding: 30px; border-radius: 15px; color: black; margin-top: 20px; }
    label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGIQUE DES PAGES ---

# --- ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:65px;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:20px;'>Amélioration du traitement de service dans les services d'urgence.</p>", unsafe_allow_html=True)

    # Statistiques
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Audits", len(df)), c2.metric("Attente Moy.", f"{round(df['attente'].mean(),1)}m"), c3.metric("Régions", df['region'].nunique())

    st.markdown("<br><h3 style='text-align:center; letter-spacing:2px;'>NAVIGUER DANS L'APPLICATION</h3>", unsafe_allow_html=True)
    
    col_n1, col_n2, col_n3 = st.columns(3)
    with col_n1:
        st.button("clic_audit", key="b_audit", on_click=lambda: changer_page("Audit"))
        st.markdown('<div class="nav-card"><div class="card-icon">📝</div><div class="card-title">AUDIT</div><div class="card-subtitle">Participer à l\'enquête</div></div>', unsafe_allow_html=True)
    with col_n2:
        st.button("clic_admin", key="b_admin", on_click=lambda: changer_page("Admin"))
        st.markdown('<div class="nav-card"><div class="card-icon">🔐</div><div class="card-title">ADMIN</div><div class="card-subtitle">Espace Enquêteur</div></div>', unsafe_allow_html=True)
    with col_n3:
        st.button("clic_infos", key="b_infos", on_click=lambda: changer_page("Infos"))
        st.markdown('<div class="nav-card"><div class="card-icon">ℹ️</div><div class="card-title">INFOS</div><div class="card-subtitle">À propos du projet</div></div>', unsafe_allow_html=True)

# --- PAGE AUDIT ---
elif st.session_state.page == "Audit":
    if st.button("⬅️ Retour"): changer_page("Accueil")
    st.markdown("## 📝 Formulaire d'Audit Patient")
    
    with st.container():
        st.markdown('<div class="white-box">', unsafe_allow_html=True)
        with st.form("audit_form"):
            c1, c2 = st.columns(2)
            nom = c1.text_input("Nom")
            prenom = c2.text_input("Prénom")
            age = st.number_input("Âge", min_value=0, max_value=120)
            region = st.selectbox("Région", list(data_cameroun.keys()))
            hopital = st.selectbox("Hôpital", data_cameroun[region])
            attente = st.slider("Temps d'attente (minutes)", 0, 300, 30)
            eval_med = st.select_slider("Évaluation Prise en charge médicale", ["Médiocre", "Passable", "Bien", "Excellent"])
            suggestions = st.text_area("Vos suggestions d'amélioration")
            
            submit = st.form_submit_button("Envoyer mon rapport")
            if submit:
                conn = get_connection()
                c = conn.cursor()
                c.execute("INSERT INTO rapports (nom, prenom, age, region, hopital, attente, eval_med, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?)",
                          (nom, prenom, age, region, hopital, attente, eval_med, suggestions, datetime.now()))
                conn.commit()
                conn.close()
                st.success("Merci ! Votre rapport a été enregistré.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE ADMIN ---
elif st.session_state.page == "Admin":
    if st.button("⬅️ Retour"): changer_page("Accueil")
    st.title("🔐 Espace Administrateur")
    
    # Simple check password
    pw = st.text_input("Code d'accès", type="password")
    if pw == "admin123":
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM rapports", conn)
        conn.close()
        st.dataframe(df)
    else:
        st.warning("Veuillez entrer le code pour voir les données.")

# --- PAGE INFOS ---
elif st.session_state.page == "Infos":
    if st.button("⬅️ Retour"): changer_page("Accueil")
    st.title("ℹ️ À propos")
    st.markdown("""
    **Patient Plus** est une initiative visant à digitaliser le suivi de la qualité des soins au Cameroun. 
    Les données collectées permettent d'identifier les goulots d'étranglement dans les services d'urgence.
    """)

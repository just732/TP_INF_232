import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
import hashlib

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus", layout="wide", initial_sidebar_state="collapsed")

# --- FONCTIONS DE SÉCURITÉ ---
def hasher_mdp(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('patient_plus_final.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS utilisateurs (username TEXT PRIMARY KEY, password TEXT, nom TEXT, prenom TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS formulaires (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, hopital TEXT, 
                    service TEXT, note INTEGER, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- STYLE CSS (BLEU NUIT & ÉLÉGANCE) ---
st.markdown("""
    <style>
    /* Global - Bleu Nuit */
    .stApp {
        background-color: #001122;
        color: #e0e0e0;
    }
    
    /* Barre de Navigation Fixe */
    .nav-bar {
        background-color: #001a33;
        padding: 10px;
        border-bottom: 2px solid #00d4ff;
    }
    
    h1, h2, h3, h4 { color: #00d4ff !important; }
    
    /* Boutons personnalisés */
    .stButton>button {
        background-color: #00d4ff !important; color: #001122 !important;
        font-weight: bold !important; border-radius: 25px !important;
        border: none !important; width: 100% !important;
    }

    /* Champs de saisie */
    input { background-color: white !important; color: black !important; border-radius: 10px !important; }
    
    /* Box pour les questions d'audit */
    .question-card {
        background-color: rgba(0, 212, 255, 0.1);
        padding: 15px; border-radius: 10px; border-left: 5px solid #00d4ff; margin-bottom: 10px;
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DE LA NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'user_connecte' not in st.session_state: st.session_state.user_connecte = None

def naviguer(nom_page):
    st.session_state.page = nom_page

# ==========================================
# BARRE DE NAVIGATION (FONCTIONNELLE)
# ==========================================
st.markdown("<div class='nav-bar'>", unsafe_allow_html=True)
cols = st.columns([2, 1, 1, 1, 1])
with cols[0]: st.markdown("<h2 style='margin:0;'>PATIENT <span style='color:white;'>PLUS</span></h2>", unsafe_allow_html=True)
if cols[1].button("ACCUEIL"): naviguer("Accueil")
if cols[2].button("SERVICES"): naviguer("Services")
if cols[3].button("STATISTIQUES"): naviguer("Stats")
if st.session_state.user_connecte:
    if cols[4].button("DÉCONNEXION"): st.session_state.user_connecte = None; naviguer("Accueil")
else:
    if cols[4].button("S'IDENTIFIER"): naviguer("Auth")
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE D'ACCUEIL : DISCOURS ET PRÉSENTATION
# ==========================================
if st.session_state.page == "Accueil":
    st.title("Votre voix peut transformer notre système de santé")
    st.markdown("""
    ### Bienvenue sur Patient Plus
    **Patient Plus** est votre plateforme citoyenne dédiée à la collecte de données sur la qualité de service des hôpitaux du Cameroun. 
    
    Notre mission est simple : **Écouter pour Améliorer**. En partageant votre expérience, vous offrez aux autorités de santé les outils nécessaires pour identifier les forces et corriger les faiblesses de nos structures hospitalières (réactivité, hygiène, sécurité, logistique).
    
    **Pourquoi répondre à nos formulaires ?**
    Votre témoignage est une pierre précieuse pour l'édifice d'une santé de qualité pour tous. Répondez avec **totale confiance** : vos données sont traitées de manière strictement confidentielle et sécurisée. Seules les tendances statistiques sont analysées pour porter votre message au plus haut niveau.
    
    **Rejoignez-nous dès maintenant et soyez acteur de l'excellence hospitalière au Cameroun !**
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg", use_column_width=True)
    
    st.markdown("<center>", unsafe_allow_html=True)
    if not st.session_state.user_connecte:
        if st.button("CRÉER MON COMPTE ET REMPLIR UN FORMULAIRE"): naviguer("Auth")
    st.markdown("</center>", unsafe_allow_html=True)

# ==========================================
# PAGE STATISTIQUES (DIAGRAMMES & CAMEMBERTS)
# ==========================================
elif st.session_state.page == "Stats":
    st.title("📊 Statistiques Nationales de Qualité")
    conn = sqlite3.connect('patient_plus_final.db')
    df = pd.read_sql_query("SELECT * FROM formulaires", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée disponible pour le moment. Les statistiques s'afficheront après les premiers formulaires.")
    else:
        st.markdown("##### Ces graphiques représentent les données collectées auprès des utilisateurs de la plateforme.")
        c1, c2 = st.columns(2)
        with c1:
            # Diagramme en barres : Note moyenne par hôpital saisi
            moyennes = df.groupby('hopital')['note'].mean().reset_index()
            fig1 = px.bar(moyennes, x='hopital', y='note', title="Moyenne de satisfaction par Hôpital", 
                          template="plotly_dark", color_discrete_sequence=['#00d4ff'])
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            # Camembert : Répartition par service
            fig2 = px.pie(df, names='service', title="Répartition des audits par Pôle", 
                          hole=0.4, template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# AUTHENTIFICATION
# ==========================================
elif st.session_state.page == "Auth":
    st.title("🔐 Espace Patient")
    choix = st.radio("Action :", ["Se connecter", "Créer un compte"])
    user = st.text_input("Identifiant (Email/Téléphone)")
    mdp = st.text_input("Mot de passe", type="password")
    
    if choix == "Créer un compte":
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        if st.button("S'INSCRIRE"):
            conn = sqlite3.connect('patient_plus_final.db'); c = conn.cursor()
            try:
                c.execute('INSERT INTO utilisateurs VALUES (?,?,?,?)', (user, hasher_mdp(mdp), nom, prenom))
                conn.commit(); st.success("Compte créé avec succès !")
            except: st.error("Identifiant déjà pris.")
            conn.close()
    else:
        if st.button("SE CONNECTER"):
            conn = sqlite3.connect('patient_plus_final.db'); c = conn.cursor()
            c.execute('SELECT * FROM utilisateurs WHERE username=? AND password=?', (user, hasher_mdp(mdp)))
            if c.fetchone():
                st.session_state.user_connecte = user
                naviguer("Formulaire"); st.rerun()
            else: st.error("Identifiants incorrects.")
            conn.close()

# ==========================================
# PAGE FORMULAIRE (DYNAMIQUE)
# ==========================================
elif st.session_state.page == "Formulaire":
    if not st.session_state.user_connecte: naviguer("Auth"); st.rerun()

    st.title("📝 Formulaire de Qualité Hospitalière")
    with st.form("form_global"):
        st.subheader("1. Informations Personnelles")
        col_id1, col_id2 = st.columns(2)
        nom_f = col_id1.text_input("Nom")
        pre_f = col_id2.text_input("Prénom")
        
        # CALENDRIER 1915 À 2026
        dob_f = col_id1.date_input("Date de naissance", 
                                   min_value=datetime(1915, 1, 1), 
                                   max_value=datetime(2026, 12, 31),
                                   value=datetime(1995, 1, 1))
        contact_f = col_id2.text_input("Contact de référence")

        st.subheader("2. Établissement et Service")
        # SAISIE LIBRE
        hopital_nom = st.text_input("Nom de l'hôpital consulté")
        service_f = st.selectbox("Sélectionnez le service visité", 
                                ["Urgence et Diagnostic", "Médecine", "Chirurgie et Soins Intensifs", "Supports et Techniques"])

        st.divider()

        # --- QUESTIONNAIRES SPÉCIFIQUES ---
        st.subheader(f"3. Questionnaire spécifique : {service_f}")

        if service_f == "Urgence et Diagnostic":
            st.markdown('<div class="question-card">Triage : Le temps d\'attente avant le premier examen infirmier est-il inférieur à 15 minutes ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Ne sais pas"], key="q1_1")
            st.markdown('<div class="question-card">Disponibilité technique : Les équipements d\'imagerie (Radio/Scanner) sont-ils fonctionnels au moment de la demande ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Pas tous"], key="q1_2")
            st.markdown('<div class="question-card">Communication : Avez-vous été informé du délai estimé avant la prise en charge médicale ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non"], key="q1_3")
            st.markdown('<div class="question-card">Sécurité : Le protocole d\'identification a-t-il été vérifié avant tout prélèvement ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non"], key="q1_4")
            st.markdown('<div class="question-card">Orientation : Le transfert vers l\'hospitalisation ou la sortie a-t-il été fluide ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Moyennement"], key="q1_5")

        elif service_f == "Médecine":
            st.markdown('<div class="question-card">Douleur : La douleur est-elle réévaluée après chaque administration de traitement ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Pas systématiquement"], key="q2_1")
            st.markdown('<div class="question-card">Information : Le médecin a-t-il expliqué le diagnostic et les risques de façon compréhensible ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Très clair", "Partiellement", "Pas du tout"], key="q2_2")
            st.markdown('<div class="question-card">Hygiène : Le personnel respecte-t-il l\'hygiène des mains avant et après chaque contact ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui, toujours", "Parfois", "Jamais remarqué"], key="q2_3")
            st.markdown('<div class="question-card">Alimentation : La qualité et la température des repas servis sont-elles satisfaisantes ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Satisfaisant", "Passable", "Médiocre"], key="q2_4")
            st.markdown('<div class="question-card">Dossier : Les constantes (tension, température) sont-elles relevées au moins 3 fois par jour ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Ne sais pas"], key="q2_5")

        elif service_f == "Chirurgie et Soins Intensifs":
            st.markdown('<div class="question-card">Check-list : La check-list "Sécurité du patient au bloc" a-t-elle été remplie pour l\'intervention ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Ne sais pas"], key="q3_1")
            st.markdown('<div class="question-card">Consentement : Le formulaire de consentement éclairé était-il signé avant l\'anesthésie ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non"], key="q3_2")
            st.markdown('<div class="question-card">Vigilance : Le ratio infirmier/patient permettait-il une surveillance constante ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Passable"], key="q3_3")
            st.markdown('<div class="question-card">Stérilisation : La traçabilité de la stérilisation a-t-elle été vérifiée devant vous ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Je ne sais pas"], key="q3_4")
            st.markdown('<div class="question-card">Infections : Un suivi des infections nosocomiales a-t-il été mentionné ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non"], key="q3_5")

        elif service_f == "Supports et Techniques":
            st.markdown('<div class="question-card">Pharmacie : Le taux de disponibilité des médicaments essentiels était-il suffisant (>90%) ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non, ruptures fréquentes"], key="q4_1")
            st.markdown('<div class="question-card">Maintenance : Les groupes électrogènes et réserves d\'eau sont-ils testés ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Ne sais pas"], key="q4_2")
            st.markdown('<div class="question-card">Propreté : Les sanitaires sont-ils nettoyés au moins deux fois par jour ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Rarement"], key="q4_3")
            st.markdown('<div class="question-card">Facturation : La facture est-elle détaillée et expliquée de manière transparente ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non", "Moyennement"], key="q4_4")
            st.markdown('<div class="question-card">Confidentialité : La discrétion de vos données a-t-elle été garantie à l\'accueil ?</div>', unsafe_allow_html=True)
            st.radio("Réponse :", ["Oui", "Non"], key="q4_5")

        st.divider()
        note_finale = st.select_slider("Note globale de satisfaction pour cette visite (1 à 5)", options=[1, 2, 3, 4, 5])
        
        if st.form_submit_button("VALIDER ET ENVOYER LE FORMULAIRE"):
            if not hopital_nom:
                st.error("Veuillez saisir le nom de l'établissement.")
            else:
                conn = sqlite3.connect('patient_plus_final.db'); c = conn.cursor()
                c.execute('INSERT INTO formulaires (user, hopital, service, note, date) VALUES (?,?,?,?,?)', 
                          (st.session_state.user_connecte, hopital_nom, service_f, note_finale, datetime.now().strftime("%Y-%m-%d")))
                conn.commit(); conn.close()
                st.success("Formulaire transmis avec succès !")
                st.balloons()
                naviguer("Stats"); st.rerun()

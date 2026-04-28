import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Patient Plus - Audit National",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Accueil"

def changer_page(nom):
    st.session_state.page = nom

# ─────────────────────────────────────────────
# DONNÉES CAMEROUN
# ─────────────────────────────────────────────
DATA_CAMEROUN = {
    "Adamaoua":    ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre":      ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé",
                    "CHU de Yaoundé", "Hôpital Gynéco-Obstétrique"],
    "Est":         ["Hôpital Régional de Bertoua", "Hôpital de District de Batouri"],
    "Extrême-Nord":["Hôpital Régional de Maroua", "Hôpital de District de Kousseri"],
    "Littoral":    ["Hôpital Général de Douala", "Hôpital Laquintinie",
                    "Hôpital de District de Bonassama"],
    "Nord":        ["Hôpital Régional de Garoua", "Hôpital de District de Guider"],
    "Nord-Ouest":  ["Hôpital Régional de Bamenda", "Hôpital de District de Wum"],
    "Ouest":       ["Hôpital Régional de Bafoussam", "Hôpital de District de Dschang"],
    "Sud":         ["Hôpital Régional d'Ebolowa", "Hôpital de District de Kribi"],
    "Sud-Ouest":   ["Hôpital Régional de Buea", "Hôpital Régional de Limbe"],
}

# ─────────────────────────────────────────────
# CONFIGURATION EMAIL (à personnaliser)
# ─────────────────────────────────────────────
EMAIL_EXPEDITEUR  = "patientplus.audit@gmail.com"   # ← votre adresse Gmail
EMAIL_MOT_DE_PASSE = "xxxx xxxx xxxx xxxx"          # ← mot de passe d'application Gmail
# Pour créer un mot de passe d'application Gmail :
# Compte Google → Sécurité → Validation en 2 étapes → Mots de passe des applications

# ─────────────────────────────────────────────
# BASE DE DONNÉES SQLITE
# ─────────────────────────────────────────────
DB_PATH = "audit_patient_plus.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    # Table des audits
    c.execute("""
        CREATE TABLE IF NOT EXISTS rapports (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nom             TEXT,
            prenom          TEXT,
            age             INTEGER,
            sexe            TEXT,
            metier          TEXT,
            dob             TEXT,
            region          TEXT,
            domicile        TEXT,
            email           TEXT,
            maladie         TEXT,
            service         TEXT,
            hopital         TEXT,
            attente         INTEGER,
            eval_inf        TEXT,
            justif_inf      TEXT,
            eval_med        TEXT,
            justif_med      TEXT,
            rdv_ligne       TEXT,
            suggestions     TEXT,
            date_soumission DATETIME
        )
    """)

    # Table des enquêteurs (code + email)
    c.execute("""
        CREATE TABLE IF NOT EXISTS enqueteurs (
            code        TEXT PRIMARY KEY,
            nom         TEXT,
            email       TEXT,
            hopital     TEXT,
            date_creation DATETIME
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ─────────────────────────────────────────────
# FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────
def generer_code():
    """Génère un code unique de type ENQ-XXXX"""
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    conn = get_conn()
    while True:
        code = "ENQ-" + "".join(random.choices(chars, k=4))
        existe = conn.execute(
            "SELECT 1 FROM enqueteurs WHERE code=?", (code,)
        ).fetchone()
        if not existe:
            conn.close()
            return code

def enregistrer_enqueteur(code, nom, email, hopital):
    conn = get_conn()
    conn.execute(
        "INSERT INTO enqueteurs (code,nom,email,hopital,date_creation) VALUES (?,?,?,?,?)",
        (code, nom, email, hopital, datetime.now())
    )
    conn.commit()
    conn.close()

def verifier_code(code):
    conn = get_conn()
    row = conn.execute(
        "SELECT nom, email, hopital FROM enqueteurs WHERE code=?", (code,)
    ).fetchone()
    conn.close()
    return {"nom": row[0], "email": row[1], "hopital": row[2]} if row else None

def lire_rapports():
    conn = get_conn()
    df = pd.read_sql_query(
        "SELECT * FROM rapports ORDER BY id DESC", conn
    )
    conn.close()
    return df

def inserer_rapport(**kwargs):
    conn = get_conn()
    conn.execute("""
        INSERT INTO rapports
        (nom,prenom,age,sexe,metier,dob,region,domicile,email,
         maladie,service,hopital,attente,eval_inf,justif_inf,eval_med,justif_med,
         rdv_ligne,suggestions,date_soumission)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        kwargs["nom"], kwargs["prenom"], kwargs["age"], kwargs["sexe"],
        kwargs["metier"], kwargs["dob"], kwargs["region"], kwargs["domicile"],
        kwargs["email"], kwargs["maladie"], kwargs["service"], kwargs["hopital"],
        kwargs["attente"], kwargs["eval_inf"], kwargs["justif_inf"],
        kwargs["eval_med"], kwargs["justif_med"], kwargs["rdv_ligne"],
        kwargs["suggestions"], datetime.now()
    ))
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
# ENVOI D'EMAIL
# ─────────────────────────────────────────────
def envoyer_email_code(destinataire, nom, code):
    """Envoie le code enquêteur par email."""
    sujet = "Patient Plus – Votre code enquêteur"
    corps = f"""
Bonjour {nom},

Votre code enquêteur Patient Plus a été créé avec succès.

╔══════════════════╗
║   {code}    ║
╚══════════════════╝

Conservez ce code précieusement. Il vous permet d'accéder
au tableau de bord des audits et de recevoir les résultats
par email après chaque soumission.

Cordialement,
L'équipe Patient Plus – Ministère de la Santé Publique du Cameroun
    """
    _envoyer(destinataire, sujet, corps)

def envoyer_email_audit(rapport: dict):
    """Envoie les résultats d'un audit à tous les enquêteurs enregistrés."""
    conn = get_conn()
    enqueteurs = conn.execute("SELECT nom, email FROM enqueteurs").fetchall()
    conn.close()

    if not enqueteurs:
        return

    sujet = f"Patient Plus – Nouvel audit : {rapport.get('hopital','')}"
    corps = f"""
Nouveau rapport d'audit soumis

─── Patient ───────────────────────────
Nom         : {rapport.get('nom','')} {rapport.get('prenom','')}
Âge         : {rapport.get('age','')} ans | Sexe : {rapport.get('sexe','')}
Région      : {rapport.get('region','')}
Hôpital     : {rapport.get('hopital','')}
Motif       : {rapport.get('maladie','')}
Service     : {rapport.get('service','')}

─── Évaluation ────────────────────────
Attente     : {rapport.get('attente','')} min
Note infirmières : {rapport.get('eval_inf','')}/5
Note médecins    : {rapport.get('eval_med','')}/5
RDV en ligne     : {rapport.get('rdv_ligne','')}

─── Suggestions ───────────────────────
{rapport.get('suggestions','(aucune)')}

Date : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
─────────────────────────────────────────
Patient Plus | Audit National Cameroun
    """
    for _, email in enqueteurs:
        _envoyer(email, sujet, corps)

def _envoyer(destinataire, sujet, corps):
    """Fonction interne d'envoi SMTP."""
    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_EXPEDITEUR
        msg["To"]      = destinataire
        msg["Subject"] = sujet
        msg.attach(MIMEText(corps, "plain", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_EXPEDITEUR, EMAIL_MOT_DE_PASSE)
            server.sendmail(EMAIL_EXPEDITEUR, destinataire, msg.as_string())
    except Exception as e:
        # Affiche en console sans bloquer l'app
        print(f"[Email] Erreur envoi vers {destinataire}: {e}")

# ─────────────────────────────────────────────
# CSS PERSONNALISÉ
# ─────────────────────────────────────────────
st.markdown("""
<style>
.stApp {
    background:
        linear-gradient(rgba(0,43,92,0.82), rgba(0,43,92,0.82)),
        url('https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
    background-size: cover;
    background-attachment: fixed;
    color: white;
}
.info-bubble {
    background: rgba(255,255,255,0.95);
    border-left: 8px solid #e1395f;
    border-radius: 16px;
    padding: 20px;
    color: #1a1a1a;
    margin-bottom: 20px;
}
.nav-card {
    background: rgba(255,255,255,0.15);
    border: 2px solid white;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    transition: 0.3s;
}
.code-box {
    background: #f0f4ff;
    border: 2px dashed #002b5c;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.stButton>button {
    background-color: #e1395f !important;
    color: white !important;
    border-radius: 50px !important;
    font-weight: bold !important;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE : ACCUEIL
# ─────────────────────────────────────────────
if st.session_state.page == "Accueil":
    st.markdown(
        "<h1 style='text-align:center;font-size:60px;'>PATIENT PLUS</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center;font-size:20px;'>Améliorer la qualité des soins dans nos services d'urgence et hospitaliers.</p>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="info-bubble">
            <h4>📊 Performance Hospitalière</h4>
            <p><b>Hôpitaux Régionaux :</b> 4 000 à 6 000 hospitalisations/an. Surcharge critique.</p>
            <p><b>Statut :</b> Seuls 48% des 172 hôpitaux publics sont jugés performants.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="info-bubble">
            <h4>👶 Maternité et Nouveau-nés</h4>
            <p><b>Accouchements :</b> 35,9% se font encore à domicile sans assistance médicale.</p>
            <p>L'audit aide à identifier les freins à l'admission institutionnelle.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align:center;'>QUE SOUHAITEZ-VOUS FAIRE ?</h2>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown('<div class="nav-card"><h3>📝 AUDIT</h3><p>Remplir le formulaire patient.</p></div>',
                    unsafe_allow_html=True)
        st.button("OUVRIR LE FORMULAIRE", on_click=lambda: changer_page("Formulaire"), key="btn_form")
    with n2:
        st.markdown('<div class="nav-card"><h3>📊 ENQUÊTEUR</h3><p>Créer / accéder à son espace.</p></div>',
                    unsafe_allow_html=True)
        st.button("ESPACE ENQUÊTEUR", on_click=lambda: changer_page("Enqueteur"), key="btn_enq")
    with n3:
        st.markdown('<div class="nav-card"><h3>ℹ️ INFOS</h3><p>En savoir plus sur Patient Plus.</p></div>',
                    unsafe_allow_html=True)
        st.button("À PROPOS", on_click=lambda: changer_page("Infos"), key="btn_info")

# ─────────────────────────────────────────────
# PAGE : FORMULAIRE
# ─────────────────────────────────────────────
elif st.session_state.page == "Formulaire":
    st.button("⬅ Retour", on_click=lambda: changer_page("Accueil"), key="back_form")
    st.markdown("<h2>📝 Formulaire d'Audit National</h2>", unsafe_allow_html=True)

    with st.form("audit_form", clear_on_submit=True):
        st.subheader("1. Identification")
        c1, c2 = st.columns(2)
        nom     = c1.text_input("Nom")
        prenom  = c2.text_input("Prénom")
        age     = c1.number_input("Âge", 0, 110, 25)
        sexe    = c2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier  = c1.text_input("Métier")
        email   = c2.text_input("Email")
        dob     = c1.date_input("Date de naissance")

        st.subheader("2. Localisation")
        region  = st.selectbox("Région du Cameroun :", list(DATA_CAMEROUN.keys()))
        hopital = st.selectbox("Hôpital fréquenté :", DATA_CAMEROUN[region])
        domicile= st.text_input("Quartier de résidence")

        st.subheader("3. Évaluation")
        maladie = st.text_input("Maladie / Motif")
        service = st.text_input("Service visité")
        attente = st.slider("Temps d'attente aux urgences (min)", 0, 300, 30)

        ci, cm = st.columns(2)
        e_inf   = ci.select_slider("Note Infirmières", options=["1","2","3","4","5"])
        j_inf   = ci.text_area("Justification Infirmières")
        e_med   = cm.select_slider("Note Médecins",     options=["1","2","3","4","5"])
        j_med   = cm.text_area("Justification Médecins")

        st.subheader("4. Suggestions")
        sug = st.text_area("Comment améliorer le service ?")
        rdv = st.radio("Prendre RDV en ligne ?", ["Oui", "Non"])

        if st.form_submit_button("✅ VALIDER L'AUDIT"):
            rapport = dict(
                nom=nom, prenom=prenom, age=age, sexe=sexe, metier=metier,
                dob=str(dob), region=region, domicile=domicile, email=email,
                maladie=maladie, service=service, hopital=hopital, attente=attente,
                eval_inf=e_inf, justif_inf=j_inf, eval_med=e_med, justif_med=j_med,
                rdv_ligne=rdv, suggestions=sug
            )
            inserer_rapport(**rapport)
            # Notifier tous les enquêteurs par email
            envoyer_email_audit(rapport)
            st.success("✅ Audit soumis ! Les enquêteurs ont été notifiés par email.")
            st.balloons()

# ─────────────────────────────────────────────
# PAGE : ENQUÊTEUR
# ─────────────────────────────────────────────
elif st.session_state.page == "Enqueteur":
    st.button("⬅ Retour", on_click=lambda: changer_page("Accueil"), key="back_enq")
    st.markdown("<h2>🔐 Espace Enquêteur</h2>", unsafe_allow_html=True)

    onglet = st.radio("", ["Créer mon code", "Accéder avec mon code"], horizontal=True)
    st.markdown("---")

    # ── CRÉER UN CODE ──────────────────────────
    if onglet == "Créer mon code":
        st.markdown("### Créer votre code enquêteur personnel")
        with st.form("form_creer_code"):
            enq_nom    = st.text_input("Votre nom complet")
            enq_email  = st.text_input("Votre email (pour recevoir les résultats)")
            enq_hopital= st.text_input("Votre hôpital / région")

            if st.form_submit_button("GÉNÉRER MON CODE"):
                if not enq_nom or not enq_email:
                    st.error("Nom et email obligatoires.")
                else:
                    code = generer_code()
                    enregistrer_enqueteur(code, enq_nom, enq_email, enq_hopital)
                    envoyer_email_code(enq_email, enq_nom, code)
                    st.markdown(f"""
                    <div class="code-box">
                        <p style='font-size:14px;color:#555;margin-bottom:8px'>Votre code personnel d'accès :</p>
                        <p style='font-size:40px;font-weight:700;color:#002b5c;letter-spacing:8px'>{code}</p>
                        <p style='font-size:13px;color:#555'>Conservez ce code. Il a été envoyé à <b>{enq_email}</b>.</p>
                        <p style='color:#0a7c42;font-weight:600'>✅ Email envoyé avec succès !</p>
                    </div>
                    """, unsafe_allow_html=True)

    # ── ACCÉDER AVEC SON CODE ──────────────────
    else:
        st.markdown("### Accéder à votre tableau de bord")
        st.info("📧 Vous recevez un email automatique après chaque soumission d'audit.")

        code_saisi = st.text_input("Votre code enquêteur (ex: ENQ-7X3K)").strip().upper()

        if st.button("ACCÉDER AU TABLEAU DE BORD"):
            enq = verifier_code(code_saisi)
            if enq:
                st.session_state["enq_valide"] = enq
            else:
                st.error("❌ Code invalide ou non reconnu.")
                st.session_state.pop("enq_valide", None)

        if "enq_valide" in st.session_state:
            enq = st.session_state["enq_valide"]
            st.success(f"Bienvenue, **{enq['nom']}** ({enq['hopital'] or 'tous hôpitaux'})")

            df = lire_rapports()

            if df.empty:
                st.info("Aucun audit enregistré pour le moment.")
            else:
                # KPIs
                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Audits soumis", len(df))
                k2.metric("Attente moyenne", f"{int(df['attente'].mean())} min")
                k3.metric("Note infirmières",
                          f"{pd.to_numeric(df['eval_inf'],errors='coerce').mean():.1f}/5")
                k4.metric("Note médecins",
                          f"{pd.to_numeric(df['eval_med'],errors='coerce').mean():.1f}/5")

                st.markdown("---")
                col_g, col_d = st.columns(2)
                with col_g:
                    st.plotly_chart(
                        px.bar(df, x="region", title="Audits par Région",
                               color_discrete_sequence=["#e1395f"]),
                        use_container_width=True
                    )
                with col_d:
                    st.plotly_chart(
                        px.box(df, x="hopital", y="attente",
                               title="Temps d'attente par Hôpital"),
                        use_container_width=True
                    )

                st.dataframe(df, use_container_width=True)

                # Export CSV
                csv = df.to_csv(index=False, sep=";", encoding="utf-8-sig")
                st.download_button(
                    "📥 Télécharger en CSV",
                    data=csv,
                    file_name=f"patient_plus_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

# ─────────────────────────────────────────────
# PAGE : INFOS
# ─────────────────────────────────────────────
elif st.session_state.page == "Infos":
    st.button("⬅ Retour", on_click=lambda: changer_page("Accueil"), key="back_info")
    st.markdown("<h2>ℹ️ À propos de Patient Plus</h2>", unsafe_allow_html=True)
    st.markdown("""
Patient Plus est une initiative nationale visant à collecter des données de satisfaction
patient dans l'ensemble des hôpitaux publics du Cameroun, afin d'orienter les politiques
d'amélioration de la qualité des soins.

**Notre mission :** Donner la parole aux patients.

**Couverture :** 10 régions du Cameroun, hôpitaux régionaux et de district.

**Accès enquêteurs :** Chaque enquêteur crée son code personnel et reçoit
les résultats par email après chaque soumission d'audit.

**Contact :** Ministère de la Santé Publique du Cameroun — Direction de l'Audit Hospitalier.
    """)

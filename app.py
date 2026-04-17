import streamlit as st
from groq import Groq
import os

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Victorine Monné - Assistant Stratégique", page_icon="📑")
st.title("🎯 Mon Assistant Stratégique Expert")

# 2. RÉCUPÉRATION DE LA CLÉ API
api_key_secret = os.getenv("GROQ_API_KEY")
if api_key_secret:
    client = Groq(api_key=api_key_secret)
else:
    st.error("⚠️ Clé API manquante dans les Secrets.")
    st.stop()

# 3. LE CERVEAU DE L'APPLICATION (Tes données fixes)
BIO_EXPERTE = "Archiviste diplômée du STIA, 8 ans d'expérience (Ministère de la Culture). Spécialiste transformation numérique et archivage Low-Cost."

MES_PROJETS_FIXES = {
    "LIKOAM": "Système de Gestion d'Archives Numériques (Apps Script/Firebase). Automatise le cycle de vie (versement, DUA, élimination). Cible: Administrations à moyens limités.",
    "Libre Outils": "Suite de micro-apps offline (DocManager, BiblioManager, PMEManager). Pas d'abonnement, données locales, fonctionne sans internet.",
    "Expertise Conseil": "Audit, formation et accompagnement en gouvernance documentaire et normes ISO."
}

GLOSSAIRE_PIAF = "DUA: Durée d'Utilité Administrative. Valeur probante: Intégrité et fiabilité. Cycle de vie: Étapes du document de la création à l'archivage final."

# 4. BARRE LATÉRALE (Sidebar)
with st.sidebar:
    st.header("👤 Mon Profil")
    st.info(f"**Bio:** {BIO_EXPERTE}")
    
    st.divider()
    st.header("📁 Gestion des Projets")
    
    # Choix entre projets existants ou nouveau
    mode_projet = st.radio("Source du projet :", ["Projet existant", "Nouveau projet +"])
    
    if mode_projet == "Projet existant":
        nom_projet = st.selectbox("Choisir un projet :", list(MES_PROJETS_FIXES.keys()))
        def_projet = MES_PROJETS_FIXES[nom_projet]
    else:
        nom_projet = st.text_input("Nom du nouveau projet", placeholder="Ex: Projet X")
        def_projet = st.text_area("Définition du projet", placeholder="Décrivez votre projet ici...")

    st.divider()
    st.caption("Base terminologique : Glossaire PIAF/AIMF intégré.")

# 5. INTERFACE PRINCIPALE
col1, col2 = st.columns(2)
with col1:
    type_contenu = st.selectbox("Format", ["Post LinkedIn", "Article Blog", "Facebook", "Script Vidéo"])
with col2:
    ton = st.selectbox("Ton", ["Expert & Professionnel", "Pédagogique", "Engagé", "Amical"])

sujet = st.text_area("Sujet du jour (ex: L'importance de la DUA)")

# 6. GÉNÉRATION
if st.button("✨ Générer le contenu"):
    if sujet and def_projet:
        # Le prompt qui fusionne tout : Code + Application + Glossaire
        prompt = f"""
        CONTEXTE EXPERT: {BIO_EXPERTE}
        TERMINOLOGIE RÉFÉRENCE: {GLOSSAIRE_PIAF}
        PROJET ACTUEL ({nom_projet}): {def_projet}
        
        FORMAT: {type_contenu}
        TON: {ton}
        SUJET: {sujet}
        
        Rédige un contenu percutant. Utilise ton expertise d'archiviste pour donner de la valeur.
        Si c'est pour LinkedIn, utilise des accroches fortes et des hashtags pertinents.
        """
        
        with st.spinner("Analyse du projet et rédaction en cours..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.session_state['resultat'] = completion.choices[0].message.content

# 7. AFFICHAGE ET TÉLÉCHARGEMENT
if 'resultat' in st.session_state:
    st.markdown("---")
    st.markdown(st.session_state['resultat'])
    st.download_button("📥 Télécharger le texte", st.session_state['resultat'], file_name=f"post_{nom_projet}.txt")

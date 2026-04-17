import streamlit as st
from groq import Groq
import os

# 1. CONFIGURATION
st.set_page_config(page_title="Victorine Monné - Stratégie", page_icon="🏛️")

# 2. ACCÈS API
api_key_secret = os.getenv("GROQ_API_KEY")
if api_key_secret:
    client = Groq(api_key=api_key_secret)
else:
    st.error("Clé API manquante.")
    st.stop()

# 3. BASE DE CONNAISSANCE (Tes sites + Glossaire)
EXPERTISE_CONTEXT = """
BIO: Victorine Monné, Archiviste (8 ans d'xp, STIA). 
PROJETS:
- LIKOAM: Archivage numérique sur Google Workspace/Firebase. Focus: Traçabilité, conformité DUA, coût réduit.
- LIBRE OUTILS: Micro-apps HTML/JS autonomes. Focus: Offline-first, vie privée (stockage local), paiement unique (pas d'abonnement).
TERMINOLOGIE PILLIER: Valeur probante, Intégrité, Cycle de vie, Versement, Échéancier de conservation (ISO 30300).
"""

# 4. BARRE LATÉRALE
with st.sidebar:
    st.header("⚙️ Configuration")
    choix_projet = st.selectbox("Projet ou Expertise", ["LIKOAM", "Libre Outils", "Expertise Conseil", "Nouveau Projet"])
    
    if choix_projet == "Nouveau Projet":
        nom_nouveau = st.text_input("Nom du nouveau projet")
        def_nouveau = st.text_area("Description rapide du projet")
        contexte_travail = f"Nouveau projet: {nom_nouveau}. Description: {def_nouveau}"
    else:
        contexte_travail = f"Focus sur {choix_projet}"

# 5. INTERFACE PRINCIPALE
st.title("🖋️ Rédaction Stratégique & Marketing")

col1, col2 = st.columns(2)
with col1:
    # Réintégration de tes tons favoris avec les miens
    ton = st.selectbox("Ton du message", 
                      ["Professionnel", "Pédagogique", "Vendeur (Publicitaire)", "Inspirant (Émotionnel)", "Visionnaire"])
with col2:
    format_post = st.selectbox("Format", ["Post LinkedIn", "Facebook", "Article de blog", "Script Vidéo"])

sujet_precis = st.text_area("Quel est l'objectif ou le sujet du message ?", 
                           placeholder="Ex: Convaincre une mairie d'adopter LIKOAM pour sécuriser ses actes...")

# 6. GÉNÉRATION
if st.button("🚀 Générer le contenu"):
    if sujet_precis:
        # Instruction système pour éviter la répétition du CV
        system_prompt = f"""
        Tu es Victorine Monné. Tu ne cites jamais ton diplôme ou tes années d'expérience explicitement sauf si c'est indispensable.
        Tu agis comme une experte qui apporte une solution concrète.
        
        CONTEXTE TECHNIQUE: {EXPERTISE_CONTEXT}
        PROJET CONCERNÉ: {contexte_travail}
        
        CONSIGNES DE TON :
        - Si 'Vendeur': Sois persuasive, insiste sur le gain de temps, d'argent et la sécurité.
        - Si 'Inspirant': Parle d'impact, d'avenir, de souveraineté numérique pour l'Afrique.
        - Si 'Pédagogique': Explique les termes du glossaire (comme la DUA) simplement.
        """
        
        user_prompt = f"""
        Sujet: {sujet_precis}
        Format: {format_post}
        Ton choisi: {ton}
        
        Action: Rédige un texte puissant. Si tu utilises des termes techniques (comme 'valeur probante'), assure-toi qu'ils servent le message.
        """

        with st.spinner("Rédaction en cours..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            st.session_state['resultat'] = completion.choices[0].message.content

# 7. AFFICHAGE
if 'resultat' in st.session_state:
    st.markdown("---")
    st.markdown(st.session_state['resultat'])
    st.download_button("📥 Télécharger", st.session_state['resultat'], file_name="contenu_expert.txt")

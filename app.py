import streamlit as st
from groq import Groq
import os

# Configuration de la page
st.set_page_config(page_title="IA Marketing CI", page_icon="🚀")
st.title("🎯 Mon Assistant Stratégique")

# Récupération sécurisée de la clé API
api_key_secret = os.getenv("GROQ_API_KEY")

if api_key_secret:
    client = Groq(api_key=api_key_secret)
else:
    st.error("⚠️ La clé API n'est pas configurée dans les Secrets de l'application.")
    st.stop()

# Barre latérale pour la personnalisation
with st.sidebar:
    st.header("👤 Mon Univers")
    ma_bio = st.text_area("Ma Bio / Mon Profil", placeholder="Qui es-tu ?")
    mon_univers = st.text_area("Mes Valeurs", placeholder="Ex: Innovation, Proximité...")
    mes_projets = st.text_area("Mes Projets", placeholder="Sur quoi travailles-tu ?")

# Interface principale
col1, col2 = st.columns(2)
with col1:
    type_contenu = st.selectbox("Format", ["Post LinkedIn", "Facebook", "Script YouTube", "Blog"])
with col2:
    ton = st.selectbox("Ton", ["Professionnel", "Amical", "Vendeur", "Inspirant"])

sujet = st.text_area("Sujet du jour")

if st.button("✨ Générer le contenu"):
    if sujet:
        prompt = f"""
        BIO: {ma_bio}
        UNIVERS: {mon_univers}
        PROJETS: {mes_projets}
        FORMAT: {type_contenu}
        TON: {ton}
        SUJET: {sujet}
        
        Rédige un contenu percutant en respectant ces éléments.
        """
        
        with st.spinner("L'IA travaille..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
            )
            st.session_state['resultat'] = completion.choices[0].message.content

# Affichage du résultat
if 'resultat' in st.session_state:
    st.markdown("---")
    st.write(st.session_state['resultat'])
    st.download_button("📥 Télécharger (.txt)", st.session_state['resultat'], "contenu.txt")

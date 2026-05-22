import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="Recrut-AI Pro", page_icon="👔", layout="wide")

# Design épuré et suppression de la sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
@import url('https://googleapis.com');
html, body, div, p, h1, h2, h3, h4, h5, h6, span {
    font-family: 'Poppins', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# CONFIGURATION PAYPAL
# -------------------------
PAYPAL_CLIENT_ID = "DEMO"  
PAYPAL_PLAN_ID = "DEMO"    

# -------------------------
# GESTION DE L'ACCÈS
# -------------------------
if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

# -------------------------
# INTERFACE SÉCURISÉE
# -------------------------
st.title("👔 Recrut-AI Pro")
st.subheader("Générez des fiches de poste de niveau expert et des guides d'entretien en 2 secondes.")

# CAS 1 : L'UTILISATEUR N'A PAS PAYÉ
if not st.session_state.est_abonne:
    st.warning("🔒 Cette application est réservée aux membres de la version Premium.")
    
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Recrutez les meilleurs pour 30 $/mois")
        st.write("Évitez les erreurs de casting qui coûtent des milliers de dollars. Générez des fiches de poste attractives et obtenez des grilles de questions d'entretien sur-mesure.")
        st.write("Le paiement est entièrement sécurisé par **PayPal**.")
        
        if PAYPAL_CLIENT_ID == "DEMO":
            paypal_html = """
            <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
                <div style="background-color: #ffc439; color: #003087; text-align: center; 
                            padding: 12px; font-family: Arial, sans-serif; font-weight: bold; 
                            border-radius: 4px; max-width: 300px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🟨 S'abonner avec PayPal (Démo)
                </div>
            </a>
            """
        else:
            paypal_html = f"""
            <div id="paypal-button-container-fixed" style="max-width: 350px; margin-top: 20px;"></div>
            <script src="https://paypal.com/sdk/js?client-id={PAYPAL_CLIENT_ID}&vault=true&intent=subscription" data-sdk-integration-source="button-factory"></script>
            <script>
              paypal.Buttons({{
                  style: {{ shape: 'rect', color: 'gold', layout: 'vertical', label: 'subscribe' }},
                  createSubscription: function(data, actions) {{
                    return actions.subscription.create({{ 'plan_id': '{PAYPAL_PLAN_ID}' }});
                  }},
                  onApprove: function(data, actions) {{
                    alert('Abonnement réussi ! ID : ' + data.subscriptionID);
                  }}
              }}).render('#paypal-button-container-fixed');
            </script>
            """
        components.html(paypal_html, height=150, scrolling=False)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        email = st.text_input("Adresse e-mail")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "recrut30":
                st.session_state.est_abonne = True
                st.success("Accès accordé !")
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

# CAS 2 : L'UTILISATEUR EST ABONNÉ -> ACCÈS COMPLÈT
else:
    st.write("✨ **Espace Recrutement Actif.** Gagnez du temps sur vos embauches.")
    if st.button("🚪 Se déconnecter", key="logout"):
        st.session_state.est_abonne = False
        st.rerun()
        
    st.write("---")

    with st.container(border=True):
        col_inputs, col_options = st.columns(2)
        
        with col_inputs:
            poste_nom = st.text_input("Intitulé du poste recherché :", placeholder="Ex: Développeur Python Junior, Commercial Sédentaire")
            competences_cles = st.text_area(
                "Compétences ou outils exigés (Optionnel) :", 
                placeholder="Ex: Maîtrise de Django, Bon niveau d'anglais, Esprit d'équipe, 2 ans d'expérience"
            )
            
        with col_options:
            outil_choix = st.selectbox("Que voulez-vous générer ?", [
                "📋 Fiche de poste complète (Attractive et claire)",
                "❓ Guide de 10 Questions d'entretien (Techniques et comportementales)",
                "🔥 Message d'approche direct (Pour chasser des candidats sur LinkedIn)"
            ])
            
            ton_entreprise = st.selectbox("Style de culture d'entreprise", [
                "🚀 Startup / Décontracté (Le 'Tu' est de rigueur)",
                "🏢 Corporate / Traditionnel (Professionnel et sérieux)",
                "🌱 Moderne / Engagé (Focus valeurs et équilibre de vie)"
            ])

        generer = st.button("🚀 Lancer la génération Recrut-AI", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Erreur : La clé GROQ_API_KEY est manquante dans les Secrets.")
        elif not poste_nom:
            st.error("⚠️ Veuillez entrer au moins l'intitulé du poste.")
        else:
            with st.spinner("L'IA de Groq prépare vos documents RH..."):
                try:
                    client = Groq(api_key=API_KEY)
                    
                    prompt_systeme = f"""Tu es un Directeur des Ressources Humaines (DRH) d'élite et un recruteur de talents internationaux.
                    Ton but est de fournir des documents de recrutement impeccables, modernes et ultra-professionnels.
                    Structure clairement ta réponse avec des titres en gras, des puces claires et des tableaux si nécessaire.
                    Respecte l'outil demandé et le style de culture d'entreprise : {ton_entreprise}.
                    Ne fais aucune introduction ni conclusion amicale, commence directement par le contenu du document demandé."""

                    prompt_utilisateur = f"""
                    Poste : {poste_nom}
                    Compétences attendues : {competences_cles}
                    Ce qu'il faut générer : {outil_choix}
                    """

                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": prompt_utilisateur}
                        ],
                        temperature=0.7
                    )
                    
                    doc_genere = reponse.choices.message.content
                    st.success("✨ Votre document RH est prêt !")
                    st.markdown(doc_genere)
                    st.text_area("Copier le texte brut :", value=doc_genere, height=300)

                except Exception as e:
                    st.error(f"Erreur technique Groq : {str(e)}")

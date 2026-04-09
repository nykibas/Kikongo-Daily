import google.generativeai as genai

# Configuration de votre clé API
genai.configure(api_key="VOTRE_CLE_API")
model = genai.GenerativeModel('gemini-1.5-flash')

def generer_contenu_du_jour():
    prompt = """
    Choisis un proverbe en langue Kikongo. 
    Donne-moi :
    1. Le proverbe original.
    2. La traduction en français.
    3. Une explication courte de la sagesse derrière (30 mots max).
    4. Un prompt détaillé pour générer une image réaliste illustrant ce proverbe.
    Formatte le tout en JSON.
    """
    response = model.generate_content(prompt)
    return response.text

# Ce JSON sera ensuite utilisé pour créer la vidéo et l'image
print(generer_contenu_du_jour())

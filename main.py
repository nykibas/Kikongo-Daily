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

import os
from google.generativeai import ImageGenerationModel

# On initialise le modèle d'image
# Note : En 2026, nous utilisons la version stable la plus récente
image_model = ImageGenerationModel("imagen-3.0-generate-001")

def generer_visuel_proverbe(description_visuelle, nom_fichier="daily_kikongo.png"):
    """
    Transforme la description de Gemini en une image haute résolution.
    """
    print(f"Génération de l'image pour : {description_visuelle}...")
    
    # On demande une image de haute qualité (proche de ce que sortirait votre D7500)
    response = image_model.generate_images(
        prompt=description_visuelle,
        number_of_images=1,
        aspect_ratio="9:16", # Format vertical idéal pour YouTube Shorts/Reels
        safety_filter_level="block_some",
        person_generation="allow_adult"
    )

    # Sauvegarde de l'image sur votre ProBook
    for i, image in enumerate(response.images):
        image.save(f"output/{nom_fichier}")
        print(f"Image sauvegardée sous output/{nom_fichier}")

# Exemple d'utilisation avec un prompt généré par Gemini
description = "Une scène paisible dans un village du Kongo central au coucher du soleil, style cinématographique, haute résolution."
generer_visuel_proverbe(description)

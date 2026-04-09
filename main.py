import os
import json
import subprocess
import google.generativeai as genai
from google.generativeai import ImageGenerationModel
# Import pour l'upload (optionnel mais inclus pour l'autonomie)
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ==========================================
# 1. CONFIGURATION ET CLÉS
# ==========================================
API_KEY = "VOTRE_CLE_API_GEMINI"
genai.configure(api_key=API_KEY)

# Initialisation des modèles
model_text = genai.GenerativeModel('gemini-1.5-flash')
model_image = ImageGenerationModel("imagen-3.0-generate-001")

# Chemins des fichiers
OUTPUT_DIR = "/home/nykibas/kikongo_project/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMAGE_TEMP = os.path.join(OUTPUT_DIR, "temp_bg.png")
VIDEO_FINAL = os.path.join(OUTPUT_DIR, "daily_kikongo.mp4")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ==========================================
# 2. GÉNÉRATION DU CONTENU (GEMINI)
# ==========================================
def obtenir_donnees_kikongo():
    print("🤖 Étape 1 : Réflexion sur le proverbe...")
    prompt = """
    Génère un contenu pour 'Kikongo Daily' au format JSON strict :
    {
      "proverbe_kikongo": "texte",
      "traduction_francaise": "texte",
      "sens_profond": "explication courte",
      "image_prompt": "prompt détaillé pour Imagen 3 (style photo cinématographique, bokeh f/1.8, lumière dorée)"
    }
    Réponds UNIQUEMENT en JSON.
    """
    response = model_text.generate_content(prompt)
    # Nettoyage du JSON (au cas où Gemini ajoute des balises ```json)
    clean_json = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_json)

# ==========================================
# 3. GÉNÉRATION DE L'IMAGE (IMAGEN 3)
# ==========================================
def generer_image(prompt_visuel):
    print("🎨 Étape 2 : Création du visuel haute résolution...")
    response = model_image.generate_images(
        prompt=prompt_visuel,
        number_of_images=1,
        aspect_ratio="9:16"
    )
    response.images[0].save(IMAGE_TEMP)
    return IMAGE_TEMP

# ==========================================
# 4. ASSEMBLAGE VIDÉO (FFMPEG)
# ==========================================
def creer_video(data):
    print("🎬 Étape 3 : Montage de la vidéo avec FFmpeg...")
    kikongo = data['proverbe_kikongo'].replace("'", "\\'") # Échappement pour FFmpeg
    traduc = data['traduction_francaise'].replace("'", "\\'")

    # Commande FFmpeg : Loop image + Zoom + Overlays Texte
    cmd = [
        'ffmpeg', '-y', '-loop', '1', '-i', IMAGE_TEMP,
        '-vf', (
            f"zoompan=z='min(zoom+0.0015,1.5)':d=250:s=1080x1920,"
            f"drawtext=fontfile={FONT_PATH}:text='{kikongo}':fontcolor=white:fontsize=70:"
            f"x=(w-text_w)/2:y=(h-text_h)/2-100:borderw=3:bordercolor=black,"
            f"drawtext=fontfile={FONT_PATH}:text='{traduc}':fontcolor=yellow:fontsize=45:"
            f"x=(w-text_w)/2:y=(h-text_h)/2+100:borderw=2:bordercolor=black"
        ),
        '-t', '10', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', VIDEO_FINAL
    ]
    
    subprocess.run(cmd, check=True)
    return VIDEO_FINAL

# ==========================================
# 5. EXECUTION PRINCIPALE
# ==========================================
def main():
    try:
        # A. On obtient les textes
        data = obtenir_donnees_kikongo()
        print(f"📖 Proverbe : {data['proverbe_kikongo']}")

        # B. On crée l'image de fond
        generer_image(data['image_prompt'])

        # C. On fabrique la vidéo
        creer_video(data)

        print(f"✅ SUCCÈS ! Vidéo générée ici : {VIDEO_FINAL}")
        
        # Ici, vous pourriez ajouter l'appel à une fonction upload_to_youtube()
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE : {str(e)}")

if __name__ == "__main__":
    main()

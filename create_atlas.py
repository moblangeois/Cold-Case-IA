from nomic import embed, AtlasDataset
import os
from PIL import Image, UnidentifiedImageError
import uuid
import numpy as np
from PyPDF2 import PdfReader

# Chemins des répertoires
CASE_DIR = "Kyron_Horman"
TEXT_DIRS = {
    "podcast_topics": os.path.join(CASE_DIR, "podcast_topics"),
    "scraped_sources": os.path.join(CASE_DIR, "scraped_sources"),
    "others": os.path.join(CASE_DIR, "texts")
}
PDF_DIR = os.path.join(CASE_DIR, "official_documents")
IMAGE_DIR = os.path.join(CASE_DIR, "images")


def load_texts():
    """Charge les fichiers texte des répertoires spécifiés et les intègre comme entrées au dataset."""
    all_text_data = []
    for category, text_dir in TEXT_DIRS.items():
        if not os.path.exists(text_dir):
            continue
        for filename in os.listdir(text_dir):
            if filename.endswith('.txt'):
                try:
                    with open(os.path.join(text_dir, filename), 'r', encoding='utf-8') as f:
                        text_content = f.read().strip()
                        all_text_data.append({
                            "type": "text",
                            "filename": f"text_{uuid.uuid4().hex[:8]}",  # Identifier unique
                            "content_type": category,
                            "content": text_content
                        })
                except Exception as e:
                    print(f"Erreur lecture fichier texte {filename}: {e}")
    return all_text_data


def load_pdfs():
    """Extrait le texte des fichiers PDF et les intègre comme entrées au dataset."""
    all_pdf_data = []
    if not os.path.exists(PDF_DIR):
        return all_pdf_data
    for filename in os.listdir(PDF_DIR):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(PDF_DIR, filename)
            try:
                reader = PdfReader(pdf_path)
                all_text = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text.strip()
                all_pdf_data.append({
                    "type": "text",
                    "filename": f"pdf_{uuid.uuid4().hex[:8]}",  # Identifier unique
                    "content_type": "official_document",
                    "content": all_text
                })
            except Exception as e:
                print(f"Impossible de lire le PDF {filename}: {str(e)}")
    return all_pdf_data


def load_images():
    """Charge les images en vérifiant les formats et les intègre comme entrées au dataset."""
    all_image_data = []
    if not os.path.exists(IMAGE_DIR):
        return all_image_data
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img_path = os.path.join(IMAGE_DIR, filename)
                with Image.open(img_path) as img:
                    img.verify()
                    # Création d'un nom unique pour chaque image
                    extension = img.format.lower() if img.format else "jpg"  # Par défaut .jpg
                    all_image_data.append({
                        "type": "image",
                        "filename": f"image_{uuid.uuid4().hex[:8]}.{extension}",  # Identifier unique
                        "content_type": "evidence",
                        "content": img_path  # Chemin absolu vers l'image
                    })
            except UnidentifiedImageError:
                print(f"Image non valide ignorée : {filename}")
    return all_image_data


def create_case_map():
    """Crée une carte multimodale combinant textes et images."""
    text_data = load_texts()
    pdf_data = load_pdfs()
    image_data = load_images()

    # Texte total = fichiers texte + PDF
    all_text_data = text_data + pdf_data
    print(f"Chargé : {len(all_text_data)} documents texte et {len(image_data)} images.")

    # Création du dataset sur Atlas
    dataset = AtlasDataset(
        identifier=f"kyron-horman-multimodal-{uuid.uuid4().hex[:8]}",
        description="Carte multimodale textes/images.",
        unique_id_field="filename",  # Identifier unique pour chaque entrée,
        is_public=True
    )

    if all_text_data:
        # Récupérer les contenus textuels
        text_contents = [item['content'] for item in all_text_data]

        # Générer les embeddings pour les textes
        text_embeddings = embed.text(
            texts=text_contents,
            model="nomic-embed-text-v1.5"
        )['embeddings']

        # Convertir en tableau NumPy 2D
        text_embeddings = np.array(text_embeddings)
        dataset.add_data(data=all_text_data, embeddings=text_embeddings)

    if image_data:
        # Générer les embeddings pour les images
        image_paths = [img['content'] for img in image_data if os.path.exists(img['content'])]

        image_embeddings = embed.image(
            images=image_paths,
            model="nomic-embed-vision-v1.5"
        )['embeddings']

        # Convertir en tableau NumPy 2D
        image_embeddings = np.array(image_embeddings)
        dataset.add_data(data=image_data, embeddings=image_embeddings)

    # Créer un index et générer un lien pour la carte
    return dataset.create_index(name="multimodal-map", modality="embedding", topic_model={"build_topic_model": True, "topic_label_field": "content"}).dataset_link


if __name__ == "__main__":
    print("Création de la carte multimodale Atlas...")
    try:
        atlas_url = create_case_map()
        print(f"Carte disponible à : {atlas_url}")
    except Exception as e:
        print(f"Erreur : {e}")
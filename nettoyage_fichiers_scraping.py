import os
import re

# Dossier contenant les fichiers à analyser
OUTPUT_DIR = "scraped_sources"

# Listes de mots-clés ou expressions à chercher pour nettoyer les fichiers
UNWANTED_PATTERNS = [
    r"Uncovered is where the most passionate true crime enthusiasts.*",  # Texte de la page par défaut d'Uncovered
    r"Sorry, we just need to make sure you're not a robot.*",  # Texte de validation "pas un robot"
    r"cookies",  # Termes relatifs aux cookies
    r"make sure your browser is accepting cookies",  # Phrase générique sur les cookies
    r"no content found",  # Texte générique pour le cas "aucun contenu"
    r"error",  # Messages d'erreur génériques
    r"please enable javascript",  # Indication d'activer JavaScript
]

def contains_unwanted_content(file_path):
    """
    Vérifie si le fichier contient des chaînes indésirables basées sur les mots-clés dans UNWANTED_PATTERNS.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            for pattern in UNWANTED_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):  # Recherche insensible à la casse
                    return True
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")
    return False

def clean_unwanted_files(output_dir):
    """
    Parcourt les fichiers du répertoire donné et supprime ceux qui contiennent uniquement des contenus indésirables.
    """
    if not os.path.exists(output_dir):
        print(f"❌ Le dossier {output_dir} n'existe pas.")
        return

    files_removed = 0
    files_checked = 0

    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)

        # Vérifier si le fichier est un fichier texte
        if os.path.isfile(file_path) and file_path.endswith(".txt"):
            files_checked += 1

            if contains_unwanted_content(file_path):
                # Supprimer le fichier s'il contient du contenu indésirable
                os.remove(file_path)
                files_removed += 1
                print(f"🗑️ Fichier supprimé : {filename}")

    print(f"\n✅ Analyse terminée. {files_removed} fichiers supprimés sur {files_checked}.")

if __name__ == "__main__":
    print("🔍 Nettoyage des fichiers indésirables...")
    clean_unwanted_files(OUTPUT_DIR)
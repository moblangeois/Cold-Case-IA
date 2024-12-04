import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Dossier de sauvegarde pour les résultats
OUTPUT_DIR = "scraped_sources"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def setup_driver():
    """Initialise le WebDriver."""
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Décommenter pour exécuter sans interface graphique
    options.add_argument('--start-maximized')
    return webdriver.Chrome(options=options)

def scrape_source_links(main_url):
    """Récupère tous les liens des sources depuis la page principale."""
    driver = setup_driver()
    driver.get(main_url)

    try:
        # Attendre que la section des sources soit visible
        print("⏳ Chargement des sections 'Sources'...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//section//h1[contains(text(), 'Sources')]"))
        )
        time.sleep(2)  # Attendre pour être sûr que tout a été chargé

        # Localiser les liens des sources
        link_elements = driver.find_elements(By.XPATH, "//section[contains(@class, 'max-w-6xl')]//a[@href]")

        links = []
        for element in link_elements:
            link = element.get_attribute("href")
            if link:  # Ajouter uniquement les liens valides
                links.append(link)

        print(f"🔗 {len(links)} liens trouvés.")
        return links

    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération des liens : {e}")
        return []

    finally:
        driver.quit()

def extract_paragraphs_from_url(url):
    """Extrait le contenu des balises <p> d'un site donné."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Vérifie si la requête est réussie

        # Analyser l'HTML avec BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")  # Trouver toutes les balises <p>

        # Filtrer et collecter le contenu des balises <p>
        return [p.get_text().strip() for p in paragraphs if p.get_text().strip()]

    except Exception as e:
        print(f"⚠️ Erreur lors de l'extraction des paragraphes de {url}: {e}")
        return []

def save_text_to_file(source_name, paragraphs):
    """Sauvegarde les paragraphes dans un fichier .txt."""
    safe_name = "".join(c if c.isalnum() else "_" for c in source_name)  # Assure un nom de fichier valide
    filepath = os.path.join(OUTPUT_DIR, f"{safe_name}.txt")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n\n".join(paragraphs))

def main():
    # URL principale du dossier "Kyron Horman" sur Uncovered
    main_url = "https://uncovered.com/cases/kyron-horman"

    # 1. Scraper les liens depuis la section sources
    print("🚀 Scraping des liens des sources...")
    source_links = scrape_source_links(main_url)

    if not source_links:
        print("❌ Aucun lien trouvé. Vérifiez l'accès au site ou les paramètres du scraping.")
        return

    print(f"🔎 {len(source_links)} liens récupérés. Début de l'extraction des contenus.")

    # 2. Visiter chaque lien et extraire les textes des balises <p>
    for index, url in enumerate(source_links):
        print(f"[{index + 1}/{len(source_links)}] Extraction des paragraphes depuis : {url}...")
        paragraphs = extract_paragraphs_from_url(url)

        if paragraphs:
            # Sauvegarder les textes extraits
            source_name = f"source_{index + 1}"  # Générer un nom basé sur le numéro
            save_text_to_file(source_name, paragraphs)
            print(f"✅ Sauvegarde réussie : {source_name}.txt")
        else:
            print(f"⚠️ Aucune donnée extraite pour {url}")

if __name__ == "__main__":
    main()
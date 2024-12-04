from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import time
import os

def setup_driver():
    """Initialise le WebDriver avec des options."""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # Maximiser la fenêtre
    driver = webdriver.Chrome(options=options)
    return driver

def click_with_javascript(driver, element):
    """Clique sur un élément avec JavaScript pour éviter des interceptions."""
    driver.execute_script("arguments[0].click();", element)

def scroll_into_view(driver, element):
    """Fait défiler jusqu'à l'élément spécifié pour s'assurer qu'il est rendu."""
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

def scrape_carousel_persons(driver):
    """Scrape toutes les cartes et gère le carrousel."""
    person_details = []  # Liste pour stocker les informations des personnes

    while True:
        try:
            # Chercher toutes les cartes visibles
            person_containers = driver.find_elements(By.XPATH, "//div[contains(@class, 'bg-white border flex')]")

            for idx, container in enumerate(person_containers):
                try:
                    # Défiler jusqu'à la carte pour s'assurer qu'elle est correctement chargée
                    scroll_into_view(driver, container)
                    time.sleep(1)

                    # Extraire le nom et le rôle depuis la carte
                    try:
                        name = container.find_element(By.TAG_NAME, "strong").text.strip()
                        role = container.find_element(By.XPATH, ".//span[contains(@class, 'text-gray-500')]").text.strip()
                    except NoSuchElementException:
                        print(f"Carte ignorée à l'index {idx} (aucun nom ou rôle trouvé).")
                        continue

                    print(f"Traitement de : {name} ({role})")

                    # Cliquer sur le bouton "View Details"
                    try:
                        view_button = container.find_element(By.XPATH, ".//button[contains(text(), 'View Details')]")
                        click_with_javascript(driver, view_button)
                        time.sleep(2)  # Attendre que la modale s'affiche
                    except NoSuchElementException:
                        print(f"Pas de bouton 'View Details' trouvé pour {name}.")
                        continue

                    # Récupérer les détails depuis la fenêtre modale
                    details_text = "Détails non disponibles."
                    try:
                        details_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'details')]")
                            )
                        )
                        details_text = details_element.text.strip()
                    except TimeoutException:
                        print(f"Détails non accessibles pour : {name}")

                    # Sauvegarder les informations récupérées
                    person_info = {
                        "name": name,
                        "role": role,
                        "details": details_text
                    }
                    person_details.append(person_info)
                    save_person_to_file(person_info)

                    # Fermer la modale
                    try:
                        close_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//button[contains(@aria-label, 'Close') or contains(@class, 'close')]")
                            )
                        )
                        click_with_javascript(driver, close_button)
                        time.sleep(1)
                    except TimeoutException:
                        print(f"Impossible de fermer la modale pour {name}. Fermeture forcée.")
                        driver.execute_script("document.body.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Escape'}));")

                except StaleElementReferenceException:
                    print("Carte non valide (élement obsolète).")
                    continue
                except Exception as e:
                    print(f"Erreur lors du traitement d'une carte : {e}")
                    continue

            # Passer à la page suivante dans le carrousel
            try:
                next_button = driver.find_element(
                    By.XPATH,
                    "//div[contains(@class, 'absolute') and contains(@class, 'right-0')]//button[contains(@aria-label, 'slide right')]"
                )
                if "disabled" in next_button.get_attribute("class"):
                    print("Fin du carrousel : bouton 'suivant' désactivé.")
                    break
                click_with_javascript(driver, next_button)
                time.sleep(2)  # Attendre que le carrousel se rafraîchisse
            except NoSuchElementException:
                print("Fin du carrousel : aucun bouton 'suivant' trouvé.")
                break
        except Exception as e:
            print(f"Erreur imprévue : {e}")
            break

    return person_details

def save_person_to_file(person_info):
    """Sauvegarde les informations d'une personne dans un fichier."""
    if not os.path.exists("person_details"):
        os.makedirs("person_details")
    filename = f"person_details/{person_info['name'].replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Nom: {person_info['name']}\n")
        f.write(f"Rôle: {person_info['role']}\n\n")
        f.write("Détails:\n")
        f.write(person_info['details'])

def main(url):
    driver = setup_driver()
    try:
        print("Chargement de la page...")
        driver.get(url)
        time.sleep(5)  # Attendre le chargement de la page
        print("Début du scraping...")
        person_details = scrape_carousel_persons(driver)
        print(f"Scraping terminé. {len(person_details)} personnes trouvées.")
    finally:
        driver.quit()

if __name__ == "__main__":
    URL = "https://uncovered.com/cases/kyron-horman#sources"
    main(URL)
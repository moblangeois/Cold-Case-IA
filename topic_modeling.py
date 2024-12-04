import json
import os
from bertopic import BERTopic
from hdbscan import HDBSCAN
import nltk
nltk.download("stopwords")

# Charger les stopwords en anglais
stopwords = nltk.corpus.stopwords.words("english")

# Charger les segments de texte à partir du JSON
def load_podcast_transcriptions(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    # Extraire les textes des segments
    segments = data.get("output", {}).get("segments", [])
    docs = [segment["text"] for segment in segments]
    return docs

def remove_stopwords(text, stopwords):
    return " ".join([word for word in text.split() if word not in stopwords])

# Fonction principale pour extraire des topics et sauvegarder dans des fichiers .txt
def process_podcast_topics(json_path, output_folder):
    # Charger les transcriptions
    docs = load_podcast_transcriptions(json_path)

    # Ajustements pour avoir plus de topics

    # Configurer l'algorithme HDBSCAN pour détecter plus de clusters
    hdbscan_model = HDBSCAN(min_cluster_size=5, # Réduction de la taille minimale des clusters
                            min_samples=2, # Réduction du seuil de voisinage
                            cluster_selection_epsilon=0.01, # Légèrement plus permissif
                            prediction_data=True)

    # Créer un modèle BERTopic avec une configuration personnalisée
    topic_model = BERTopic(hdbscan_model=hdbscan_model, nr_topics=None)

    # Prétraiter les documents
    docs = [remove_stopwords(doc, stopwords) for doc in docs]

    # Entraîner le modèle et récupérer les topics
    topics, probs = topic_model.fit_transform(docs)

    # Créer un dossier pour les fichiers .txt
    os.makedirs(output_folder, exist_ok=True)

    # Obtenir les documents associés à chaque topic
    doc_info = topic_model.get_document_info(docs)

    # Organiser les documents par topics
    topic_dict = {}
    for doc, info in zip(docs, doc_info["Topic"]):
        topic_id = info  # Récupérer l'ID du topic
        if topic_id not in topic_dict:
            topic_dict[topic_id] = []
        topic_dict[topic_id].append(doc)

    # Sauvegarder chaque topic dans un fichier texte distinct
    for topic_id, topic_docs in topic_dict.items():
        topic_file = os.path.join(output_folder, f"podcast_topic_{topic_id}.txt")
        with open(topic_file, "w", encoding="utf-8") as f:
            f.write("\n".join(topic_docs))
        print(f"Fichier sauvegardé : {topic_file}")

    # Visualiser les topics pour aider le débogage
    print(topic_model.get_topic_info())

# Chemins des fichiers
json_path = "podcast.json"  # Remplacez par le chemin de votre fichier JSON
output_folder = "podcast_topics"  # Dossier pour les fichiers .txt

# Appeler la fonction de traitement
process_podcast_topics(json_path, output_folder)
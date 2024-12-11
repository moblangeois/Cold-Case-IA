# Cold Case IA

Un outil d'investigation assistée par IA pour l'analyse de cold cases, démontré à travers l'étude de l'affaire Kyron Horman.

![Démonstration de l'outil](demonstration.gif)

https://atlas.nomic.ai/data/encyclopedia-uca/kyron-horman-multimodal-0f9be3a4

## 🎯 Objectif

Ce projet vise à démontrer comment l'IA peut assister les enquêteurs dans l'analyse de cold cases en :
- Centralisant et structurant les informations disponibles
- Permettant une exploration interactive des données via une carte sémantique
- Facilitant la découverte de connexions entre les éléments de l'enquête

## 🛠️ Fonctionnalités

- **Collecte automatisée** : Scripts de scraping pour rassembler les informations depuis diverses sources
- **Traitement multimodal** : Analyse de textes, documents PDF et images
- **Visualisation interactive** : Carte sémantique générée via Nomic Atlas
- **Analyse thématique** : Extraction automatique des topics des transcriptions de podcasts
- **Interface de requêtes** : Système RAG (Retrieval Augmented Generation) pour explorer les données

## 📦 Structure du projet

```
Cold-Case-IA/
│
├── create_atlas.py          # Création de la carte sémantique
├── nettoyage_fichiers_scraping.py    # Nettoyage des données
├── scraping_persons_uncovered.py     # Extraction des informations sur les personnes
├── scraping_sources_uncovered.py     # Collecte des sources
├── topic_modeling.py        # Analyse thématique des podcasts
│
└── Kyron_Horman/           # Données structurées du cas
    ├── images/             # Photos et documents visuels
    ├── official_documents/ # Documents officiels
    ├── podcast_topics/     # Analyses thématiques
    ├── scraped_sources/    # Sources web
    └── texts/             # Textes et transcriptions
```

## 🚀 Installation

1. Cloner le repository :
```bash
git clone https://github.com/moblangeois/Cold-Case-IA.git
```

## 💻 Utilisation

1. Collecte des données :
```bash
python scraping_sources_uncovered.py
python scraping_persons_uncovered.py
```

2. Nettoyage et structuration :
```bash
python nettoyage_fichiers_scraping.py
```

3. Création de la carte sémantique :
```bash
python create_atlas.py
```

## ⚠️ Note importante

Ce projet est une démonstration technique. L'implémentation dans le fichier `app.py` n'est pas présente en raison d'une protection du droit d'auteur.
De plus, l'utilisation de l'IA dans le contexte d'enquêtes criminelles soulève des questions éthiques et légales importantes. Consultez toujours les autorités compétentes.

## 📄 Licence

MIT License

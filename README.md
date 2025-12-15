# Cold Case IA

Un outil d'investigation assistée par IA pour l'analyse de cold cases, démontré à travers l'étude de l'affaire Kyron Horman.

![Démonstration de l'outil](demonstration.gif)

## Nouvelle Application Web avec Claude Sonnet 4.5

**[QUICKSTART - Lancez l'application en 5 minutes](./QUICKSTART.md)**

Cette repository contient maintenant une application web complète moderne :

- **Chat intelligent** avec Claude Sonnet 4.5
- **Recherche sémantique** dans tous les documents
- **Exploration interactive** des preuves et témoignages
- **Interface moderne** responsive avec Next.js et TailwindCSS
- **Système RAG** pour des réponses précises basées sur les sources

### Démarrage Rapide

```bash
# 1. Cloner
git clone https://github.com/moblangeois/Cold-Case-IA.git
cd Cold-Case-IA

# 2. Configurer (ajouter votre clé API Anthropic)
cp .env.example .env
nano .env

# 3. Lancer
./start.sh
```

**Accès :** http://localhost:3000

**Documentation :**
- [Guide de démarrage rapide](./QUICKSTART.md)
- [Documentation complète](./APP_README.md)
- [Guide de déploiement](./DEPLOYMENT.md)

---

## Objectif Original

Ce projet vise à démontrer comment l'IA peut assister les enquêteurs dans l'analyse de cold cases en :
- Centralisant et structurant les informations disponibles
- Permettant une exploration interactive des données via chat IA et carte sémantique
- Facilitant la découverte de connexions entre les éléments de l'enquête

**Carte sémantique Nomic Atlas :** https://atlas.nomic.ai/data/encyclopedia-uca/kyron-horman-multimodal-0f9be3a4

## Fonctionnalités

### Application Web (Nouvelle)
- **Chat avec Claude Sonnet 4.5** : Interface conversationnelle pour interroger le cas
- **Système RAG** : Recherche et synthèse automatique dans tous les documents
- **Exploration de documents** : Navigation dans textes, PDFs, images et transcriptions
- **Interface moderne** : Design responsive avec Next.js 15 et TailwindCSS
- **API REST** : Accès programmatique aux fonctionnalités

### Scripts d'Analyse (Original)
- **Collecte automatisée** : Scripts de scraping pour rassembler les informations depuis diverses sources
- **Traitement multimodal** : Analyse de textes, documents PDF et images
- **Visualisation interactive** : Carte sémantique générée via Nomic Atlas
- **Analyse thématique** : Extraction automatique des topics des transcriptions de podcasts

## Structure du projet

```
Cold-Case-IA/
│
├── backend/                 # API FastAPI avec Claude Sonnet 4.5
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── services/       # Claude API & RAG
│   │   └── models/         # Schémas Pydantic
│   └── Dockerfile
│
├── frontend/               # Interface Next.js 15
│   ├── app/
│   │   ├── page.tsx       # Accueil
│   │   ├── chat/          # Chat avec Claude
│   │   └── cases/         # Exploration
│   └── Dockerfile
│
├── nginx/                  # Reverse proxy et SSL
│   └── nginx.conf
│
├── Kyron_Horman/          # Données structurées du cas
│   ├── images/            # Photos et documents visuels
│   ├── official_documents/ # Documents officiels
│   ├── podcast_topics/    # Analyses thématiques
│   ├── scraped_sources/   # Sources web
│   └── texts/             # Textes et transcriptions
│
├── create_atlas.py        # [Original] Création de la carte sémantique
├── topic_modeling.py      # [Original] Analyse thématique
├── scraping_*.py          # [Original] Scripts de collecte
│
├── docker-compose.yml     # Orchestration des services
├── QUICKSTART.md          # Guide de démarrage rapide
├── APP_README.md          # Documentation complète
└── DEPLOYMENT.md          # Guide de déploiement production
```

## Installation et Utilisation

### Application Web (Recommandé)

**Installation rapide avec Docker :**

```bash
# 1. Cloner le repository
git clone https://github.com/moblangeois/Cold-Case-IA.git
cd Cold-Case-IA

# 2. Configuration
cp .env.example .env
# Éditer .env et ajouter votre clé API Anthropic

# 3. Lancer l'application
./start.sh

# Accès : http://localhost:3000
```

**Voir :** [QUICKSTART.md](./QUICKSTART.md) pour le guide complet

### Scripts Python Originaux

**Pour utiliser les scripts d'analyse :**

```bash
# Installation
pip install -r backend/requirements.txt

# 1. Collecte des données
python scraping_sources_uncovered.py
python scraping_persons_uncovered.py

# 2. Nettoyage
python nettoyage_fichiers_scraping.py

# 3. Analyse thématique
python topic_modeling.py

# 4. Carte sémantique
python create_atlas.py
```

## Technologies

### Stack Moderne
- **Backend** : FastAPI, Python 3.11, Anthropic Claude API
- **Frontend** : Next.js 15, React, TypeScript, TailwindCSS
- **IA** : Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
- **RAG** : ChromaDB, Sentence Transformers, LangChain
- **Infrastructure** : Docker, Nginx, Let's Encrypt

### Déploiement
- **Local** : Docker Compose
- **Production** : coldcase.citadelle.work (voir [DEPLOYMENT.md](./DEPLOYMENT.md))

## Notes importantes

### Utilisation Responsable
Ce projet est une **démonstration technique**. L'utilisation de l'IA dans le contexte d'enquêtes criminelles soulève des questions éthiques et légales importantes :

- Usage éducatif et recherche
- Démonstration de capacités de l'IA
- Analyse de sources publiques
- Ne remplace pas une enquête officielle
- Consultez toujours les autorités compétentes

### Vie Privée et Respect
- Toutes les informations proviennent de sources publiques
- Respectez la vie privée des personnes mentionnées
- L'IA peut faire des erreurs - vérifiez toujours les informations
- En espérant que ce type de technologie puisse aider à résoudre ce cas et d'autres similaires

## Licence

MIT License

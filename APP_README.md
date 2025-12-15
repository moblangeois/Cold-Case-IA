# Cold Case IA - Application Web

Application web moderne d'investigation assistée par IA utilisant Claude Sonnet 4.5.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Claude](https://img.shields.io/badge/Claude-Sonnet%204.5-purple)

## 🌟 Fonctionnalités

### 🤖 Chat Intelligent avec Claude Sonnet 4.5
- Interface de conversation interactive avec l'IA la plus avancée d'Anthropic
- Système RAG (Retrieval Augmented Generation) pour des réponses basées sur les documents
- Citations automatiques des sources utilisées
- Historique de conversation persistant

### 🔍 Système de Recherche Avancé
- Recherche sémantique dans tous les documents du cas
- Embeddings vectoriels avec Sentence Transformers
- Base de données vectorielle ChromaDB pour des recherches rapides
- Filtrage par type de contenu (podcasts, documents officiels, sources web)

### 📚 Exploration de Documents
- Navigation intuitive dans tous les documents du cas
- Prévisualisation de textes, PDFs et images
- Téléchargement de fichiers
- Statistiques détaillées sur le cas

### 🎨 Interface Moderne
- Design responsive avec TailwindCSS
- Mode sombre élégant
- Animations fluides
- Optimisé pour desktop et mobile

## 🏗️ Architecture Technique

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/          # Endpoints REST
│   │   ├── chat.py   # Chat avec Claude
│   │   ├── cases.py  # Gestion des cas
│   │   └── files.py  # Gestion des fichiers
│   ├── services/     # Logique métier
│   │   ├── claude_service.py    # API Anthropic
│   │   └── embeddings.py        # RAG & ChromaDB
│   ├── models/       # Modèles Pydantic
│   └── main.py       # Application principale
├── Dockerfile
└── requirements.txt
```

**Technologies :**
- FastAPI : Framework web moderne et performant
- Anthropic SDK : Intégration Claude Sonnet 4.5
- ChromaDB : Base de données vectorielle
- Sentence Transformers : Génération d'embeddings
- LangChain : Orchestration RAG

### Frontend (Next.js 15)
```
frontend/
├── app/
│   ├── page.tsx           # Page d'accueil
│   ├── chat/page.tsx      # Interface de chat
│   └── cases/[id]/page.tsx # Exploration de cas
├── components/            # Composants réutilisables
├── lib/
│   └── api.ts            # Client API
├── Dockerfile
└── package.json
```

**Technologies :**
- Next.js 15 : Framework React avec App Router
- TypeScript : Type safety
- TailwindCSS : Styling moderne
- Axios : Client HTTP
- React Markdown : Rendu des réponses de Claude
- Lucide React : Icônes

### Infrastructure
```
nginx/
└── nginx.conf    # Reverse proxy et SSL

docker-compose.yml  # Orchestration
```

**Technologies :**
- Docker & Docker Compose : Conteneurisation
- Nginx : Reverse proxy, SSL, load balancing

## 🚀 Installation Rapide

### Prérequis
- Docker et Docker Compose
- Clé API Anthropic (Claude Sonnet 4.5)

### Démarrage

1. **Cloner le repository**
```bash
git clone https://github.com/moblangeois/Cold-Case-IA.git
cd Cold-Case-IA
```

2. **Configuration**
```bash
# Copier les fichiers d'environnement
cp .env.example .env

# Éditer .env et ajouter votre clé API
nano .env
```

Ajouter :
```env
ANTHROPIC_API_KEY=sk-ant-api03-votre-clé-ici
```

3. **Lancer l'application**
```bash
docker-compose up -d --build
```

4. **Accéder à l'application**
- Frontend : http://localhost:3000
- Backend API : http://localhost:8000
- Documentation API : http://localhost:8000/docs

## 📖 Utilisation

### Chat avec Claude

1. Accédez à http://localhost:3000/chat
2. Posez une question sur le cas Kyron Horman
3. Claude analysera les documents pertinents et répondra
4. Les sources utilisées apparaissent dans la barre latérale

**Exemples de questions :**
- "Qui est Kyron Horman et que lui est-il arrivé ?"
- "Quelles sont les personnes clés dans cette affaire ?"
- "Quelle est la chronologie des événements ?"
- "Quels sont les principaux indices disponibles ?"

### Explorer le Cas

1. Accédez à http://localhost:3000/cases/kyron_horman
2. Consultez les statistiques du cas
3. Recherchez dans les documents
4. Filtrez par type de contenu
5. Téléchargez les fichiers

### API REST

Documentation interactive : http://localhost:8000/docs

**Endpoints principaux :**

```bash
# Chat
POST /api/chat/
{
  "message": "Qui est Kyron Horman?",
  "case_id": "kyron_horman",
  "use_rag": true
}

# Recherche
POST /api/cases/search
{
  "query": "disparition",
  "case_id": "kyron_horman",
  "limit": 5
}

# Lister les cas
GET /api/cases/

# Lister les documents
GET /api/files/documents?content_type=official_documents
```

## 🎯 Cas d'Usage

### Pour les Enquêteurs
- Centraliser toutes les informations d'un cold case
- Rechercher rapidement des informations spécifiques
- Découvrir des connexions entre différents éléments
- Générer des résumés et chronologies

### Pour les Chercheurs
- Analyser des patterns dans les cold cases
- Tester des hypothèses avec l'aide de l'IA
- Documenter et organiser les recherches

### Pour l'Éducation
- Démonstration de l'IA appliquée à l'investigation
- Étude de cas réels
- Apprentissage de techniques d'analyse

## 🔐 Sécurité

### Données
- Toutes les données restent locales (pas d'envoi au cloud sauf API Claude)
- Embeddings stockés localement avec ChromaDB
- Conversations non sauvegardées de manière permanente

### API
- CORS configuré pour domaines autorisés uniquement
- Rate limiting recommandé en production
- HTTPS obligatoire en production

### Bonnes Pratiques
- Ne jamais commiter la clé API
- Utiliser des secrets managers en production
- Limiter l'accès réseau aux services
- Mettre à jour régulièrement les dépendances

## 📊 Performance

### Optimisations Backend
- Embeddings mis en cache dans ChromaDB
- Recherche vectorielle optimisée (< 100ms)
- Pooling de connexions
- Async/await pour concurrence

### Optimisations Frontend
- Next.js App Router avec streaming
- Images optimisées automatiquement
- Code splitting automatique
- Standalone output pour Docker

### Scalabilité
- Backend stateless (scalable horizontalement)
- ChromaDB peut gérer millions de documents
- Nginx pour load balancing
- Possible d'ajouter Redis pour les sessions

## 🧪 Développement

### Backend local
```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend local
```bash
cd frontend
npm install
npm run dev
```

### Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 🌐 Déploiement Production

Voir [DEPLOYMENT.md](./DEPLOYMENT.md) pour le guide complet.

**Étapes principales :**
1. Configurer DNS pour coldcase.citadelle.work
2. Obtenir certificats SSL (Let's Encrypt)
3. Configurer variables d'environnement
4. Lancer avec docker-compose
5. Configurer monitoring et backups

## 🔄 Mises à Jour

```bash
# Arrêter l'application
docker-compose down

# Récupérer les mises à jour
git pull

# Reconstruire et redémarrer
docker-compose up -d --build
```

## 🐛 Troubleshooting

### Backend ne démarre pas
```bash
# Vérifier les logs
docker-compose logs backend

# Causes communes :
# - Clé API manquante ou invalide
# - Port 8000 déjà utilisé
# - Problème ChromaDB (supprimer le volume)
```

### Frontend ne peut pas se connecter
```bash
# Vérifier l'URL de l'API
docker-compose exec frontend env | grep API_URL

# Doit être : http://backend:8000 (dans Docker)
#         ou http://localhost:8000 (dev local)
```

### Recherche lente
```bash
# Réindexer ChromaDB
docker-compose stop backend
docker volume rm coldcase-ia_chroma_data
docker-compose up -d backend
```

## 📚 Documentation Complète

- [Guide de Déploiement](./DEPLOYMENT.md)
- [Documentation API](http://localhost:8000/docs) (après lancement)
- [Architecture Backend](./backend/README.md)
- [Architecture Frontend](./frontend/README.md)

## 🤝 Contribution

Ce projet est une démonstration technique. Les contributions sont bienvenues :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

## ⚖️ Considérations Éthiques

**Important :** Ce projet est une démonstration technique de l'application de l'IA à l'investigation.

- Respectez toujours la vie privée des personnes mentionnées
- Ne partagez pas d'informations sensibles ou non publiques
- Consultez les autorités compétentes pour les enquêtes réelles
- L'IA peut faire des erreurs - vérifiez toujours les informations

## 📄 Licence

MIT License - voir [LICENSE](./LICENSE)

## 🙏 Remerciements

- **Anthropic** pour l'API Claude Sonnet 4.5
- **Communauté open-source** pour les outils utilisés
- **Kyron Horman** - En espérant que ce type de technologie puisse aider à résoudre son cas et d'autres similaires

## 📞 Contact

Pour questions ou support :
- Ouvrir une issue sur GitHub
- Email : [votre-email]

---

**Note :** Cette application est à usage éducatif et démonstratif. Elle ne remplace pas une enquête professionnelle menée par les autorités compétentes.

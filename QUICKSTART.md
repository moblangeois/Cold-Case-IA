# 🚀 Démarrage Rapide - Cold Case IA

Guide de démarrage en 5 minutes pour l'application web Cold Case IA avec Claude Sonnet 4.5.

## Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé
- Une clé API Anthropic (Claude) - [Obtenir ici](https://console.anthropic.com/)

## Installation en 3 étapes

### 1️⃣ Récupérer le projet

```bash
git clone https://github.com/moblangeois/Cold-Case-IA.git
cd Cold-Case-IA
```

### 2️⃣ Configurer votre clé API

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env
nano .env  # ou utilisez votre éditeur préféré
```

Remplacer `your_anthropic_api_key_here` par votre vraie clé API :
```env
ANTHROPIC_API_KEY=sk-ant-api03-VOTRE_CLE_ICI
```

### 3️⃣ Lancer l'application

**Option A - Script automatique (recommandé) :**
```bash
./start.sh
```

**Option B - Commande manuelle :**
```bash
docker-compose up -d --build
```

## ✅ C'est prêt !

Ouvrez votre navigateur :
- **Application** : http://localhost:3000
- **API Docs** : http://localhost:8000/docs

## 🎯 Premiers pas

1. **Page d'accueil** : http://localhost:3000
   - Découvrez les fonctionnalités
   - Vue d'ensemble du cas Kyron Horman

2. **Chat avec Claude** : http://localhost:3000/chat
   - Posez des questions sur le cas
   - Exemples :
     - "Qui est Kyron Horman ?"
     - "Quelle est la chronologie des événements ?"
     - "Quelles sont les personnes clés dans cette affaire ?"

3. **Explorer les documents** : http://localhost:3000/cases/kyron_horman
   - Parcourir tous les documents
   - Rechercher dans les fichiers
   - Consulter les statistiques

## 📊 Vérifier que tout fonctionne

```bash
# Voir les logs en temps réel
docker-compose logs -f

# Vérifier le statut des services
docker-compose ps

# Tester l'API
curl http://localhost:8000/health
```

## 🛑 Arrêter l'application

```bash
# Option A - Script
./stop.sh

# Option B - Commande
docker-compose down
```

## ⚠️ Problèmes courants

### "Cannot connect to backend"
```bash
# Vérifier que le backend est démarré
docker-compose ps

# Redémarrer si nécessaire
docker-compose restart backend
```

### "API key not found"
```bash
# Vérifier que .env existe et contient la clé
cat .env | grep ANTHROPIC_API_KEY

# Devrait afficher : ANTHROPIC_API_KEY=sk-ant-...
```

### "Port already in use"
```bash
# Modifier les ports dans docker-compose.yml
# Par exemple, changer "3000:3000" en "3001:3000"
```

## 📚 Documentation complète

- [README complet](./APP_README.md) - Architecture et utilisation détaillée
- [Guide de déploiement](./DEPLOYMENT.md) - Production et coldcase.citadelle.work
- [API Documentation](http://localhost:8000/docs) - Endpoints REST interactifs

## 💡 Conseils

### Performance
- **Première indexation** : Le backend prend 1-2 minutes au premier démarrage pour indexer tous les documents. C'est normal !
- **Réponses de Claude** : Comptez 5-15 secondes pour une réponse (selon la complexité)

### Utilisation
- **Conversations** : Les conversations ne sont pas sauvegardées après redémarrage
- **Sources** : Claude cite automatiquement ses sources dans la barre latérale
- **RAG** : Le système recherche dans ~100+ documents pour chaque question

### Développement
```bash
# Voir les logs d'un service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend

# Reconstruire après des modifications
docker-compose up -d --build

# Accéder au conteneur
docker-compose exec backend bash
```

## 🎓 Exemple de session

```
Vous : "Qui est Kyron Horman ?"

Claude : "Kyron Horman est un garçon de 7 ans qui a disparu le 4 juin 2010
de son école élémentaire Skyline à Portland, Oregon. Il était en deuxième
année et participait ce jour-là à une foire scientifique. Sa belle-mère,
Terri Horman, l'a accompagné à l'école vers 8h45 et a pris une photo de
lui devant son projet scientifique. C'est la dernière fois qu'il a été vu.

[Sources: transcription_podcast_episode_1.txt, official_report_2010.pdf]"
```

## 🚀 Prochaines étapes

Une fois l'application lancée :

1. ✅ Testez le chat avec différentes questions
2. ✅ Explorez les documents disponibles
3. ✅ Consultez les statistiques du cas
4. ✅ Lisez la [documentation complète](./APP_README.md)
5. ✅ Découvrez l'[API REST](http://localhost:8000/docs)

## 🆘 Besoin d'aide ?

- **Logs** : `docker-compose logs -f`
- **Documentation** : [APP_README.md](./APP_README.md)
- **Issues** : [GitHub Issues](https://github.com/moblangeois/Cold-Case-IA/issues)

---

**Bon usage ! 🔍**

*Note : Cette application est une démonstration technique. Utilisez-la de manière responsable et respectueuse.*

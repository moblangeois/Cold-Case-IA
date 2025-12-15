# Guide de Déploiement - Cold Case IA

Application web moderne pour l'investigation assistée par IA avec Claude Sonnet 4.5.

## 🏗️ Architecture

L'application est composée de trois services :

- **Backend (FastAPI)** : API RESTful avec intégration Claude Sonnet 4.5 et système RAG
- **Frontend (Next.js 15)** : Interface utilisateur moderne avec TailwindCSS
- **Nginx** : Reverse proxy et gestion SSL

## 📋 Prérequis

- Docker et Docker Compose installés
- Clé API Anthropic (Claude Sonnet 4.5)
- Accès au domaine `coldcase.citadelle.work`
- Certificats SSL pour le domaine

## 🚀 Déploiement Local (Développement)

### 1. Configuration

```bash
# Copier les fichiers d'exemple
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Éditer .env et ajouter votre clé API Anthropic
nano .env
```

Ajouter votre clé API :
```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 2. Lancement

```bash
# Construire et démarrer tous les services
docker-compose up --build

# Ou en arrière-plan
docker-compose up -d --build
```

L'application sera accessible à :
- Frontend : http://localhost:3000
- Backend API : http://localhost:8000
- Documentation API : http://localhost:8000/docs

### 3. Initialisation des données

Au premier démarrage, le backend va automatiquement :
1. Indexer tous les documents du dossier `Kyron_Horman`
2. Créer une base de données vectorielle avec ChromaDB
3. Générer les embeddings pour la recherche sémantique

Cela peut prendre quelques minutes. Vérifiez les logs :
```bash
docker-compose logs -f backend
```

## 🌐 Déploiement Production (coldcase.citadelle.work)

### 1. Préparation du serveur

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Installer Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Cloner le repository
git clone https://github.com/moblangeois/Cold-Case-IA.git
cd Cold-Case-IA
```

### 2. Configuration SSL

```bash
# Créer le répertoire SSL
mkdir -p nginx/ssl

# Option A : Utiliser Let's Encrypt (Recommandé)
sudo apt install certbot
sudo certbot certonly --standalone -d coldcase.citadelle.work

# Copier les certificats
sudo cp /etc/letsencrypt/live/coldcase.citadelle.work/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/coldcase.citadelle.work/privkey.pem nginx/ssl/key.pem

# Option B : Certificats auto-signés (Développement uniquement)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem \
  -subj "/CN=coldcase.citadelle.work"
```

### 3. Variables d'environnement

```bash
# Créer le fichier .env
cat > .env << EOF
ANTHROPIC_API_KEY=votre_clé_api_anthropic
APP_ENV=production
CORS_ORIGINS=https://coldcase.citadelle.work
EOF
```

### 4. Configuration DNS

Assurez-vous que votre DNS pointe vers votre serveur :
```
coldcase.citadelle.work.  A  votre_ip_serveur
```

### 5. Lancement en production

```bash
# Construire et démarrer
docker-compose up -d --build

# Vérifier les logs
docker-compose logs -f

# Vérifier le statut
docker-compose ps
```

### 6. Renouvellement SSL automatique

```bash
# Créer un script de renouvellement
cat > /etc/cron.monthly/renew-ssl << 'EOF'
#!/bin/bash
certbot renew --quiet
cp /etc/letsencrypt/live/coldcase.citadelle.work/fullchain.pem /path/to/Cold-Case-IA/nginx/ssl/cert.pem
cp /etc/letsencrypt/live/coldcase.citadelle.work/privkey.pem /path/to/Cold-Case-IA/nginx/ssl/key.pem
docker-compose -f /path/to/Cold-Case-IA/docker-compose.yml restart nginx
EOF

chmod +x /etc/cron.monthly/renew-ssl
```

## 🔧 Maintenance

### Mise à jour de l'application

```bash
# Arrêter l'application
docker-compose down

# Récupérer les dernières modifications
git pull origin main

# Reconstruire et redémarrer
docker-compose up -d --build
```

### Sauvegarde des données

```bash
# Sauvegarder la base de données vectorielle
docker run --rm -v coldcase-ia_chroma_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/chroma_backup_$(date +%Y%m%d).tar.gz -C /data .

# Restaurer
docker run --rm -v coldcase-ia_chroma_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/chroma_backup_YYYYMMDD.tar.gz -C /data
```

### Réinitialiser l'index vectoriel

```bash
# Arrêter le backend
docker-compose stop backend

# Supprimer les données ChromaDB
docker volume rm coldcase-ia_chroma_data

# Redémarrer (réindexation automatique)
docker-compose up -d backend
```

### Logs et monitoring

```bash
# Voir tous les logs
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx

# Statistiques de ressources
docker stats
```

## 🧪 Tests

### Test du backend

```bash
# Healthcheck
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs

# Test chat
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Qui est Kyron Horman?", "case_id": "kyron_horman"}'
```

### Test du frontend

```bash
# Vérifier que l'interface se charge
curl http://localhost:3000

# Vérifier la page de chat
open http://localhost:3000/chat
```

## 📊 Monitoring

### Health Checks

Les health checks sont configurés dans Docker Compose :

```bash
# Vérifier le statut de santé
docker-compose ps
```

### Métriques

Pour surveiller les performances :

```bash
# Utilisation CPU/RAM
docker stats

# Logs d'erreurs
docker-compose logs | grep -i error
```

## 🔒 Sécurité

### Bonnes pratiques

1. **Clé API** : Ne jamais commiter la clé API Anthropic
2. **SSL** : Toujours utiliser HTTPS en production
3. **Firewall** : Configurer un firewall (ufw)
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```
4. **Mises à jour** : Maintenir Docker et les images à jour
5. **Backups** : Sauvegarder régulièrement ChromaDB

### Limiter l'accès

Si vous souhaitez restreindre l'accès :

```nginx
# Dans nginx.conf, ajouter une authentification basique
location / {
    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://frontend;
}
```

## 🐛 Dépannage

### Le backend ne démarre pas

```bash
# Vérifier les logs
docker-compose logs backend

# Problèmes courants :
# - Clé API manquante : vérifier .env
# - Port déjà utilisé : modifier dans docker-compose.yml
# - Erreur ChromaDB : supprimer le volume et redémarrer
```

### Le frontend ne se connecte pas au backend

```bash
# Vérifier les variables d'environnement
docker-compose exec frontend env | grep API_URL

# Doit afficher : NEXT_PUBLIC_API_URL=http://backend:8000
```

### Erreurs SSL

```bash
# Vérifier les certificats
ls -la nginx/ssl/

# Permissions correctes
chmod 644 nginx/ssl/cert.pem
chmod 600 nginx/ssl/key.pem
```

### Problèmes de CORS

Si vous rencontrez des erreurs CORS, vérifiez :
1. `CORS_ORIGINS` dans `.env`
2. Configuration Nginx dans `nginx/nginx.conf`
3. Configuration FastAPI dans `backend/app/main.py`

## 📈 Scaling

Pour gérer plus de charge :

```yaml
# Ajouter dans docker-compose.yml
backend:
  deploy:
    replicas: 3
    resources:
      limits:
        cpus: '2'
        memory: 4G
```

## 📚 Ressources

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Next.js](https://nextjs.org/docs)
- [Documentation Anthropic Claude](https://docs.anthropic.com/)
- [Documentation ChromaDB](https://docs.trychroma.com/)

## 💡 Support

Pour toute question ou problème :
1. Vérifier les logs : `docker-compose logs -f`
2. Consulter cette documentation
3. Ouvrir une issue sur GitHub

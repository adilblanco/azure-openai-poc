## Guide rapide — Azure OpenAI (Étudiant)
### Objectif
Créer une ressource Azure OpenAI, déployer un modèle et tester un prompt.

### 1. Création de la ressource
1. Aller dans Azure Portal
2. Cliquer sur Créer une ressource
3. Chercher : Azure OpenAI ou Azure AI services
4. Remplir :
    * Groupe de ressources (ex): `rg-azure-ai-student`
    * Nom (ex): `adil-ai-service`
    * Région (ex): `canadacentral`
    * Niveau tarifaire: `Standard S0`
5. Créer

<img src="./figures/Screenshot 2026-05-21 at 11.23.16.png" width="400">

<img src="./figures/Screenshot 2026-05-21 at 14.08.02.png" width="400">

## 2. Comprendre la ressource

```
Une ressource Azure OpenAI = Un service qui te donne accès à l’API (pas un modèle)
Ressource =! modèle
```

### 3. Accéder à la ressource
1. Accéder à la ressource
2. Explorer les modèles Foundry

<img src="./figures/Screenshot 2026-05-21 at 11.47.28.png" width="400">

### 4. Choisir un modèle

1. Dans Model catalog
2. Choisir un modèle: `gpt-5-mini`

<img src="./figures/Screenshot 2026-05-21 at 12.23.45.png" width="400">

### 5. Déployer le modèle

1. Cliquer sur le modèle → Deploy
2. Remplir :
    * Deployment name: `mon-gpt-5-mini`
    * Deployment type: `Standard`
3. Déploiement réussi

<img src="./figures/Screenshot 2026-05-21 at 12.52.50.png" width="400">

### 6. Tester
1. Open in playground
2. Prompt: `Bonjour, explique moi Azure OpenAI`

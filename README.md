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

## Setup

### 1. Prérequis système

- Python 3.10+
- [poppler](https://poppler.freedesktop.org/) (requis par `pdf2image` pour convertir les PDFs en images)

```bash
# macOS
brew install poppler

# Ubuntu/Debian
apt-get install poppler-utils
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet :

```
AZURE_OPENAI_API_KEY=xxx
AZURE_OPENAI_ENDPOINT=https://<ressource>.openai.azure.com/openai/v1
AZURE_OPENAI_DEPLOYMENT_NAME=mon-gpt-5-mini
```

### 4. Configurer project_config.yaml

Les paramètres clés à ajuster :

| Paramètre | Emplacement | Description |
|---|---|---|
| `max_tokens` | `backend.params` | Tokens max pour la réponse — mettre suffisamment haut (ex: 4000) |
| `default_max_pages` | `pipeline` | Nombre de pages max à analyser par PDF |
| `min_confidence` | `pipeline` | Seuil de confiance minimum (0-1) |
| `label_descriptions` | `pipeline` | Types de documents à valider et leurs critères |

### 5. Lancer l'API

```bash
python app.py
```

API accessible à : http://localhost:5001

## Tester l'API

### Via curl

```bash
curl -X POST http://localhost:5001/predict \
  --form 'file=@rapport.pdf' \
  --form 'expected_type=rapport_expert'
```

### Via Python

```python
import requests

with open("rapport.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:5001/predict",
        files={"file": f},
        data={"expected_type": "rapport_expert"}
    )
    
print(response.json())
```

## Classes principales

### AzureOpenAIBackend (backend.py)

```python
backend = AzureOpenAIBackend(
    api_key="xxx",
    endpoint="https://...",
    deployment="gpt-4o-mini",
    temperature=0,
    max_tokens=1000
)

response = backend.predict(
    system_prompt="Tu es...",
    user_prompt="Valide ce document..."
)
# -> {"is_expected_type": true, "confidence": 0.92, "reason": "..."}
```

### DocumentClassificationPipeline (pipeline.py)

```python
pipeline = DocumentClassificationPipeline(
    backend=backend,
    label_descriptions={"rapport_expert": "Rapport d'un expert..."},
    min_confidence=0.85
)

result = pipeline.predict(
    file_bytes=open("rapport.pdf", "rb").read(),
    filename="rapport.pdf",
    expected_type="rapport_expert"
)
# -> {"is_expected_type": true, "confidence": 0.92, "reason": "..."}
```

### ProjectConfigLoader (project_config_loader.py)

```python
loader = ProjectConfigLoader("project_config.yaml")
config = loader.load()

backend = config["BACKEND"]
pipeline = config["PIPELINE"]
```

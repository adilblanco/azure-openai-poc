import logging
import os
import yaml
from pathlib import Path
from backend import AzureOpenAIBackend
from pipeline import DocumentClassificationPipeline

logger = logging.getLogger(__name__)


class ProjectConfigLoader:

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = None

    def load(self):
        self._load_yaml()
        backend = self._build_backend()
        pipeline = self._build_pipeline(backend)
        return {
            "BACKEND": backend,
            "PIPELINE": pipeline,
            "PROJECT_META": self.config.get("project_meta", {}),
        }

    def _load_yaml(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config YAML non trouvée: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        if not self.config:
            raise ValueError("Le fichier YAML est vide ou malformé")

    def _build_backend(self):
        backend_cfg = self.config.get("backend", {})

        if backend_cfg.get("type") != "azure_openai_llm":
            raise ValueError("Seul azure_openai_llm est supporté")

        params = backend_cfg.get("params", {})

        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

        if not all([api_key, endpoint, deployment_name]):
            raise ValueError(
                "Variables d'environnement manquantes: "
                "AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME"
            )

        logger.info(f"Backend initialisé: deployment={deployment_name}")
        return AzureOpenAIBackend(
            api_key=api_key,
            endpoint=endpoint,
            deployment=deployment_name,
            temperature=backend_cfg.get("temperature", 1),
            max_tokens=params.get("max_tokens", 1000),
            timeout=backend_cfg.get("timeout", 60),
            reasoning_effort=backend_cfg.get("reasoning_effort"),
        )

    def _build_pipeline(self, backend):
        pipeline_cfg = self.config.get("pipeline", {})

        if pipeline_cfg.get("type") != "document_classification":
            raise ValueError("Seul document_classification est supporté")

        label_descriptions = pipeline_cfg.get("label_descriptions", {})
        if not label_descriptions:
            raise ValueError("Aucune description de document définie")

        return DocumentClassificationPipeline(
            backend=backend,
            label_descriptions=label_descriptions,
            min_confidence=pipeline_cfg.get("min_confidence", 0.85),
            default_max_pages=pipeline_cfg.get("default_max_pages", 10),
        )


def load_project_config():
    config_path = os.getenv("PROJECT_CONFIG_PATH")

    if not config_path:
        local_path = Path("project_config.yaml")
        if local_path.exists():
            config_path = str(local_path.absolute())
        else:
            raise FileNotFoundError(
                "Aucun fichier project_config.yaml trouvé. "
                "Définir PROJECT_CONFIG_PATH ou placer le fichier dans le répertoire courant."
            )

    logger.info(f"Chargement config: {config_path}")
    return ProjectConfigLoader(config_path).load()

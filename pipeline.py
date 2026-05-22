import base64
import io
import logging
import os
import tempfile

import fitz
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)


class DocumentClassificationPipeline:

    def __init__(self, backend, label_descriptions, min_confidence=0.85, default_max_pages=10):
        self.backend = backend
        self.label_descriptions = label_descriptions
        self.min_confidence = min_confidence
        self.default_max_pages = default_max_pages

    def predict(self, file_bytes, filename, expected_type):
        text = self._extract_text(file_bytes, filename, self.default_max_pages)
        logger.info(f"Texte extrait: {len(text)} caractères depuis {filename!r}")

        images = self._extract_images(file_bytes, filename)
        logger.info(f"Images extraites: {len(images)} images depuis {filename!r}")

        criteria = self.label_descriptions.get(expected_type, "")
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(text, expected_type, criteria)

        llm_response = self.backend.predict(system_prompt, user_prompt, images=images)

        is_valid = (
            llm_response.get("is_expected_type", False) and
            llm_response.get("confidence", 0) >= self.min_confidence
        )

        return {
            "is_expected_type": is_valid,
            "confidence": llm_response.get("confidence", 0),
            "reason": llm_response.get("reason", "Aucune raison fournie"),
        }

    def _extract_text(self, file_bytes, filename, max_pages=None):
        if not filename.lower().endswith(".pdf"):
            return f"[Fichier image: {filename}]"

        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            pages = doc if max_pages is None else doc[:max_pages]
            text = "".join(page.get_text() + "\n" for page in pages)
            return text.strip() or "[PDF vide ou non-textuel]"
        except Exception as e:
            logger.error(f"Erreur lecture PDF {filename!r}: {e}")
            return f"[Erreur lecture PDF: {str(e)}]"


    def _extract_images(self, file_bytes, filename):
        if not filename.lower().endswith(".pdf"):
            return []

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            images_pil = convert_from_path(tmp_path, dpi=150, last_page=self.default_max_pages)

            images = []
            for img in images_pil:
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="JPEG")
                img_b64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
                images.append({"mime": "image/jpeg", "content": img_b64})
            return images

        except Exception as e:
            logger.warning(f"Erreur extraction images {filename!r}: {e}")
            return []
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def _build_system_prompt(self):
        return (
            "Tu es un expert en validation de documents administratifs. "
            "Tu dois vérifier si un document correspond à un type attendu. "
            "Tu réponds UNIQUEMENT en JSON valide."
        )

    def _build_user_prompt(self, text, expected_type, criteria):
        return f"""
            Valide si ce document est un '{expected_type}'.

            Critères à vérifier :
            {criteria}

            Contenu du document :
            {text}

            Réponds STRICTEMENT en JSON :
            {{
            "is_expected_type": true | false,
            "confidence": nombre entre 0 et 1,
            "reason": "justification factuelle, critère par critère"
            }}
        """

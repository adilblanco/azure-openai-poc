"""
Exemple d'utilisation directe (sans Flask)
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from project_config_loader import ProjectConfigLoader


def main():
    """Teste le pipeline directement."""

    # Charger les variables d'environnement
    load_dotenv()

    print("Chargement de la configuration...")
    loader = ProjectConfigLoader("project_config.yaml")
    config = loader.load()

    pipeline = config["PIPELINE"]
    print(f"Pipeline charge: {pipeline}")

    # Exemple 1: Test avec un fichier PDF
    pdf_path = Path("exemple_rapport.pdf")

    if pdf_path.exists():
        print(f"\nTest avec {pdf_path}...")

        with open(pdf_path, "rb") as f:
            result = pipeline.predict(
                file_bytes=f.read(),
                filename=pdf_path.name,
                expected_type="rapport_expert"
            )

        print("\nResultat:")
        print(f"  is_expected_type: {result['is_expected_type']}")
        print(f"  confidence: {result['confidence']}")
        print(f"  reason: {result['reason']}")

    else:
        print(f"Fichier {pdf_path} non trouve")

    # Exemple 2: Test avec du texte fictif
    print("\nTest avec texte fictif...")

    fake_pdf_bytes = b"""
RAPPORT D'EXPERTISE ARBORICOLE

Date de l'inspection: 15 mai 2026
Expert: Jean Dupont, Membre SIAQ, Certifie ISA
Adresse: 1234 Rue de l'Arbre, Montreal

Essences a abattre:
- Frene blanc: diametre 45cm, etat de sante: mauvais
- Erable: diametre 30cm, etat de sante: acceptable

Raison: Frene atteint d'une maladie virulente
Signature electronique presente
"""

    result = pipeline.predict(
        file_bytes=fake_pdf_bytes,
        filename="fake_rapport.pdf",
        expected_type="rapport_expert"
    )

    print("\nResultat:")
    print(f"  is_expected_type: {result['is_expected_type']}")
    print(f"  confidence: {result['confidence']}")
    print(f"  reason: {result['reason']}")


if __name__ == "__main__":
    main()

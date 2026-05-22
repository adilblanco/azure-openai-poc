import logging
from flask import Flask, request, jsonify
from project_config_loader import load_project_config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

try:
    config = load_project_config()
    pipeline = config["PIPELINE"]
    logger.info("Pipeline initialisé avec succès")
except Exception as e:
    logger.error(f"Erreur initialisation pipeline: {e}")
    pipeline = None


@app.route("/predict", methods=["POST"])
def predict():
    if not pipeline:
        return jsonify({"status": "error", "message": "Pipeline non initialisé"}), 500

    if "file" not in request.files:
        return jsonify({"status": "error", "message": "Aucun fichier fourni"}), 400

    file = request.files["file"]
    expected_type = request.form.get("expected_type")

    if not expected_type:
        return jsonify({"status": "error", "message": "expected_type manquant"}), 400

    logger.info(f"Prédiction: fichier={file.filename!r}, expected_type={expected_type!r}")

    try:
        result = pipeline.predict(
            file_bytes=file.read(),
            filename=file.filename,
            expected_type=expected_type
        )
        logger.info(f"Résultat: is_expected_type={result['is_expected_type']}, confidence={result['confidence']}")
        return jsonify({"status": "ok", "result": result}), 200

    except ValueError as e:
        return jsonify({"status": "error", "message": f"Erreur validation: {str(e)}"}), 400
    except Exception as e:
        logger.error(f"Erreur serveur: {e}")
        return jsonify({"status": "error", "message": f"Erreur serveur: {str(e)}"}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

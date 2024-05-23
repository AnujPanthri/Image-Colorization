from comet_ml.api import API
from src.utils.config_loader import constants

api = API()

# set env variable COMET_API_KEY

api.download_registry_model(
    "anujpanthri",
    "image-colorization-model",
    version="1.0.0",
    output_path=constants.ARTIFACT_MODEL_DIR,
    expand=True,
    stage=None, 
)
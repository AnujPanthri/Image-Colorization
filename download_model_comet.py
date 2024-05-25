from comet_ml.api import API
from src.utils.config_loader import constants
import argparse

def set_api_and_download_model(key:str, version:str, output_dir=constants.ARTIFACT_MODEL_DIR):
    api = API(api_key=key)

    # set env variable COMET_API_KEY

    api.download_registry_model(
        "anujpanthri",
        "image-colorization-model",
        version=version,
        output_path=output_dir,
        expand=True,
        stage=None, 
    )


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--key",type=str,required=True)
    parser.add_argument("--version",type=str,required=True)
    config = parser.parse_args()
    set_api_and_download_model(config.key,config.version)
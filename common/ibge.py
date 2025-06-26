import os
import json
import requests
from common import execute_query
import logging

logger = logging.getLogger("my_app")

IBGE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios?view=nivelado"


def ingest_ibge_data(data_dir="data"):
    logger.info("Ingesting IBGE data...")

    ibge_path = os.path.join(data_dir, "ibge.json")

    logger.info("Downloading IBGE data...")
    response = requests.get(IBGE_URL)
    if response.status_code == 200:
        with open(ibge_path, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        logger.info("IBGE data downloaded successfully.")
    else:
        logger.error(f"Failed to download IBGE data: {response.status_code}")
        return

    execute_query(
        f"""
        CREATE OR REPLACE TABLE ibge_municipios AS 
        SELECT * FROM read_json_auto('{ibge_path}', ignore_errors=true)
        """
    )

    logger.info("IBGE data ingested successfully.")

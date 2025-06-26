import os
import requests
import zipfile
from common import clean_csv, clean_xlsx, DatabaseConnection
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger("common")

CAD_UNICO_URL = "https://www.mds.gov.br/webarquivos/publicacao/sagi/microdados/01_cadastro_unico/base_amostra_cad_201812.zip"
DATA_DICTIONARY_URL = "https://aplicacoes.mds.gov.br/sagi/dicivip_datain/ckfinder/userfiles/files/Dicionario_base_identificada_pt_R03.xlsx"


def ingest_cad_unico_data(data_dir="data", database="database.duckdb"):
    logger.info("Ingesting CAD Unico data...")

    zip_path = os.path.join(data_dir, "base_amostra_cad_201812.zip")

    logger.info("Downloading CAD Unico data...")
    response = requests.get(CAD_UNICO_URL, stream=True)
    if response.status_code != 200:
        logger.error(
            f"Failed to download CAD Unico data: {response.status_code}")
        return
    logger.info("CAD Unico data downloaded successfully.")

    with open(zip_path, "wb") as f:
        logger.info("Saving CAD Unico data to disk...")
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
        logger.info("CAD Unico data saved successfully.")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        logger.info("Extracting CAD Unico data...")
        zip_ref.extractall(data_dir)
        logger.info("CAD Unico data extracted successfully.")

    path_pessoa = os.path.join(
        data_dir, "base_amostra_cad_201812/base_amostra_pessoa_201812.csv"
    )
    path_familia = os.path.join(
        data_dir, "base_amostra_cad_201812/base_amostra_familia_201812.csv"
    )

    with ThreadPoolExecutor() as executor:
        logger.info("Cleaning CAD Unico CSV files...")
        executor.submit(clean_csv, path_pessoa)
        executor.submit(clean_csv, path_familia)
    logger.info("CAD Unico CSV files cleaned successfully.")

    conn = DatabaseConnection(database)

    conn.execute(f"""
        CREATE OR REPLACE TABLE pessoas AS 
        SELECT * FROM read_csv('{path_pessoa}', delim=';', header=true, ignore_errors=true)
    """)

    conn.execute(f"""
        CREATE OR REPLACE TABLE familias AS 
        SELECT * FROM read_csv('{path_familia}', delim=';', header=true, ignore_errors=true)
    """)

    logger.info("CAD Unico data ingested successfully.")


def ingest_data_dictionary(data_dir="data"):
    logger.info("Ingesting CAD Unico data dictionary...")

    dict_path = os.path.join(
        data_dir, "Dicionario_base_identificada_pt_R03.xlsx"
    )

    logger.info("Downloading data dictionary...")
    response = requests.get(DATA_DICTIONARY_URL)
    if response.status_code != 200:
        logger.error(
            f"Failed to download data dictionary: {response.status_code}"
        )
        return
    logger.info("Data dictionary downloaded successfully.")

    with open(dict_path, "wb") as f:
        f.write(response.content)

    clean_xlsx(dict_path)

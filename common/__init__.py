from common.csv_cleaner import clean_csv
from common.xlsx_cleaner import clean_xlsx
from common.database import execute_query
from common.ibge import ingest_ibge_data
from common.cad_unico import ingest_cad_unico_data, ingest_data_dictionary

import os
import logging

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True
            )
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)
logger.propagate = False
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


log_file = os.path.join(LOG_DIR, 'app.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

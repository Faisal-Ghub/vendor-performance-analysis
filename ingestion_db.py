import pandas as pd
import os
import numpy as np
from sqlalchemy import create_engine
import logging
import time

os.makedirs("Logs", exist_ok=True)

logging.basicConfig(
    filename="Logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///inventory.db')

def ingest_file(df, table_name, engine):
    first = True
    
    for chunk in pd.read_csv(df, chunksize=100000):
        if first:
            chunk.to_sql(table_name, engine, if_exists='replace', index=False)
            first = False
        else:
            chunk.to_sql(table_name, engine, if_exists='append', index=False)

def load_raw_data():
    start_time = time.time()
    
    for file in os.listdir('Data'):
        file_path = 'Data/' + file
        logging.info(f"Ingesting {file} in db")
        ingest_file(file_path, file[:-4], engine)
    
    end_time = time.time()
    total_time = (end_time - start_time) / 60
    
    logging.info("-----------------Ingestion Complete-----------------")
    logging.info(f"Total Time Taken : {total_time} minutes")
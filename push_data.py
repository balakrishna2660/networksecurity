import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract:

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            records = list(json.loads(data.T.to_json()).values())

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )

            db = self.mongo_client[database]
            collection = db[collection]

            collection.insert_many(records)

            return len(records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":

    FILE_PATH = r"Network_Data\phisingData.csv"

    DATABASE = "BALAAI"

    COLLECTION = "networkdata"

    network_obj = NetworkDataExtract()

    records = network_obj.csv_to_json_convertor(FILE_PATH)

    print(f"Total Records: {len(records)}")

    no_of_records = network_obj.insert_data_mongodb(
        records,
        DATABASE,
        COLLECTION
    )

    print(f"{no_of_records} records inserted successfully.")
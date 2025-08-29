"""
Script to preprocess and insert books into MongoDB.
"""

from preprocessing import BookPreprocessor
from pymongo import MongoClient

# Parameters
CSV_PATH = "books.csv"
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "library"
COLLECTION_NAME = "books"

def main():
    """
    Preprocess the CSV file and insert the documents into MongoDB.
    """
    # Preprocessing
    preproc = BookPreprocessor(CSV_PATH)
    preproc.clean_data()
    docs = preproc.format_for_mongodb()
    print(f"{len(docs)} documents ready to be inserted into MongoDB.")

    # MongoDB connection
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Insert (replace collection if it already exists)
    collection.drop()
    result = collection.insert_many(docs)
    print(f"Insertion complete. {len(result.inserted_ids)} documents inserted into the '{COLLECTION_NAME}' collection.")

if __name__ == "__main__":
    main()
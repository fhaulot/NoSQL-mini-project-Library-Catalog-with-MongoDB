# Script pour prétraiter et insérer les livres dans MongoDB
from preprocessing import BookPreprocessor
from pymongo import MongoClient

# Paramètres
CSV_PATH = "books.csv"
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "library"
COLLECTION_NAME = "books"

def main():
	# Prétraitement
	preproc = BookPreprocessor(CSV_PATH)
	preproc.clean_data()
	docs = preproc.format_for_mongodb()
	print(f"{len(docs)} documents prêts à être insérés dans MongoDB.")

	# Connexion MongoDB
	client = MongoClient(MONGO_URI)
	db = client[DB_NAME]
	collection = db[COLLECTION_NAME]

	# Insertion (remplace la collection si elle existe déjà)
	collection.drop()
	result = collection.insert_many(docs)
	print(f"Insertion terminée. {len(result.inserted_ids)} documents insérés dans la collection '{COLLECTION_NAME}'.")

if __name__ == "__main__":
	main()

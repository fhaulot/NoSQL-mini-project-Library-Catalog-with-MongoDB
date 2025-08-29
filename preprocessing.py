"""
Preprocessing module for book data.
Loads, cleans, and formats book data for MongoDB insertion.
"""

import pandas as pd
from datetime import datetime

class BookPreprocessor:
    """
    A class to preprocess book data from a CSV file for MongoDB.
    """

    def __init__(self, file_path):
        """
        Initialize the preprocessor with the path to the CSV file.
        Loads the CSV into a pandas DataFrame.
        Args:
            file_path (str): Path to the CSV file.
        """
        self.file_path = file_path
        self.df = pd.read_csv(file_path)

    def clean_data(self):
        """
        Remove duplicates and fill missing values with empty strings.
        """
        self.df = self.df.drop_duplicates()
        self.df = self.df.fillna("")

    def format_for_mongodb(self):
        """
        Selects and formats the relevant columns for MongoDB insertion.
        - Keeps only: title, author, rating, genres, firstPublishDate.
        - Converts firstPublishDate to year (int).
        - Converts rating to float and stores as a list in 'ratings'.
        - Converts genres to a list.
        - Formats author as a dict with 'name' (and optionally 'birth_year').
        Returns:
            list: List of dictionaries ready for MongoDB insertion.
        """
        books = []
        for _, row in self.df.iterrows():
            # Title
            title = str(row.get("title", "")).strip()

            # Author
            author_name = str(row.get("author", "")).strip()
            author = {"name": author_name}
            # Optionally add birth_year if present in CSV
            if "birth_year" in row and row["birth_year"]:
                try:
                    author["birth_year"] = int(row["birth_year"])
                except Exception:
                    pass

            # Genres
            genres = row.get("genres", "")
            if isinstance(genres, str):
                genres_list = [g.strip() for g in genres.split(",") if g.strip()]
            elif isinstance(genres, list):
                genres_list = genres
            else:
                genres_list = []

            # Year
            first_publish = row.get("firstPublishDate", "")
            year = None
            if first_publish:
                try:
                    year = int(str(first_publish)[:4])
                except Exception:
                    year = None

            # Ratings
            rating = row.get("rating", "")
            try:
                rating_float = float(rating)
                ratings = [rating_float]
            except Exception:
                ratings = []

            book = {
                "title": title,
                "author": author,
                "genres": genres_list,
                "year": year,
                "ratings": ratings
            }
            books.append(book)
        return books
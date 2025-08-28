

"""
Preprocessing module for book data.
Loads, cleans, and formats book data for MongoDB insertion.
"""
    
import pandas as pd
from datetime import datetime
import ast

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
        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        self.df = self.df.drop_duplicates()
        self.df = self.df.fillna("")
        return self.df

    def select_columns(self, columns):
        """
        Keep only the specified columns in the DataFrame.
        Args:
            columns (list): List of column names to keep.
        Returns:
            pd.DataFrame: DataFrame with selected columns.
        """
        self.df = self.df[columns]
        return self.df

    @staticmethod
    def extract_year(date_str):
        """
        Extract the year as int from a date string.
        Args:
            date_str (str): Date string (e.g., '2001-05-12').
        Returns:
            int or None: Year as integer, or None if not parsable.
        """
        try:
            return int(datetime.strptime(str(date_str)[:4], "%Y").year)
        except Exception:
            return None

    @staticmethod
    def to_float(val):
        """
        Convert a value to float.
        Args:
            val: Value to convert.
        Returns:
            float or None: Converted float, or None if not possible.
        """
        try:
            return float(val)
        except Exception:
            return None

    @staticmethod
    def to_list(val):
        """
        Convert a value to a list. If already a list, return as is.
        If string, split by comma or parse as Python list.
        Args:
            val: Value to convert.
        Returns:
            list: List of strings.
        """
        if isinstance(val, list):
            return val
        if pd.isna(val) or val == '':
            return []
        if isinstance(val, str):
            try:
                parsed = ast.literal_eval(val)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass
            return [g.strip() for g in val.split(',') if g.strip()]
        return []

    @staticmethod
    def author_dict(name):
        """
        Format author as a dictionary with 'name' key.
        Args:
            name (str): Author name.
        Returns:
            dict: Author dictionary.
        """
        return {"name": name} if name else {}

    def format_for_mongodb(self):
        """
        Format the DataFrame for MongoDB insertion.
        Keeps only relevant columns and formats each field as required.
        Returns:
            list: List of dictionaries ready for MongoDB insertion.
        """
        cols = ['title', 'author', 'rating', 'genres', 'firstPublishDate']
        df = self.df[cols].copy()
        df['year'] = df['firstPublishDate'].apply(self.extract_year)
        df['rating'] = df['rating'].apply(self.to_float)
        df['genres'] = df['genres'].apply(self.to_list)
        df['title'] = df['title'].astype(str)
        df['author'] = df['author'].astype(str)
        df['ratings'] = df['rating'].apply(lambda x: [x] if x is not None else [])
        df['author'] = df['author'].apply(self.author_dict)
        records = df.apply(lambda row: {
            "title": row['title'],
            "author": row['author'],
            "genres": row['genres'],
            "year": row['year'],
            "ratings": row['ratings']
        }, axis=1).tolist()
        return records

from preprocessing import BookPreprocessor

preproc = BookPreprocessor("books.csv")
preproc.clean_data()
docs = preproc.format_for_mongodb()
# docs est une liste de dictionnaires prêts à insérer dans MongoDB
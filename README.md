# 📚 NoSQL Mini-Project: Library Catalog with MongoDB

## Overview

This project demonstrates how to build a simple library catalog using MongoDB and Python.  
It covers data preprocessing, document modeling, data insertion, and querying using PyMongo.

## Project Structure

- `preprocessing.py`: Preprocesses the CSV data and formats it for MongoDB.
- `storing.py`: Loads the preprocessed data into MongoDB.
- `mongodb.ipynb`: Jupyter notebook for running queries and updates on the MongoDB collection.
- `books.csv`: The dataset (not included in this repo for copyright reasons).

## Getting Started

### 1. Requirements

- Python 3.8+
- pandas
- pymongo
- Docker (for running MongoDB locally)

### 2. Setup MongoDB with Docker

Start a MongoDB container:
```bash
docker run -d -p 27017:27017 --name mongodb mongo:6.0
```

### 3. Preprocess and Insert Data

Activate your virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas pymongo
```

Preprocess and insert data:
```bash
python storing.py
```

### 4. Run Queries

Open `mongodb.ipynb` and run the cells to explore and update your library catalog.

## Example Document Structure

```json
{
  "title": "The Hobbit",
  "author": {"name": "J.R.R. Tolkien", "birth_year": 1892},
  "genres": ["Fantasy"],
  "year": 1937,
  "ratings": [5, 4, 5, 5]
}
```

## Features

- Flexible document model with embedded author info
- Data cleaning and normalization
- Example queries and aggregations
- Update operations (add ratings, update genres, etc.)

## License

This project is open source and free to use for educational purposes.
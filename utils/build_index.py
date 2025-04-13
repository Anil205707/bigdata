from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
import os, json

# Define the schema (structure of each document)
schema = Schema(id=ID(stored=True), title=TEXT(stored=True), abstract=TEXT(stored=True))


# Create index folder if not exists
if not os.path.exists("search_index"):
    os.mkdir("search_index")

# Create the index
ix = create_in("search_index", schema)
writer = ix.writer()

# Load your sample dataset
with open("data/cord19_sample.json", "r", encoding="utf-8") as f:
    articles = json.load(f)
    for i, article in enumerate(articles):
        writer.add_document(
            id=str(i),
            title=article.get("title", ""),
            abstract=article.get("abstract", "")
        )

writer.commit()
print("Search index created successfully!")

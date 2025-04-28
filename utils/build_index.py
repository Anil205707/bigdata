import os
import json
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in

def create_index():
    # Define schema
    schema = Schema(id=TEXT(stored=True), title=TEXT(stored=True), abstract=TEXT(stored=True))

    # Create search_index folder if it doesn't exist
    if not os.path.exists("search_index"):
        os.mkdir("search_index")

    # Create index
    ix = create_in("search_index", schema)
    writer = ix.writer()

    # Load COVID-19 dataset
    with open("data/covid19_sample_500.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    for i, article in enumerate(articles):
        writer.add_document(
            id=str(i),
            title=article.get("title", ""),
            abstract=article.get("abstract", "")
        )

    writer.commit()
    print("✅ Search index created successfully!")


if __name__ == "__main__":
    create_index()

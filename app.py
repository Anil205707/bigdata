from flask import Flask, render_template, request
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
import os

app = Flask(__name__)

# Check if search_index exists, else create it
if not os.path.exists("search_index") or not os.listdir("search_index"):
    from utils.build_index import create_index
    create_index()

# Now open the existing index
index = open_dir("search_index")

@app.route("/", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        query_text = request.form.get("query")
        with index.searcher() as searcher:
            parser = MultifieldParser(["title", "abstract"], schema=index.schema)
            query = parser.parse(query_text)
            search_results = searcher.search(query, limit=10)
            results = [dict(title=hit["title"], abstract=hit["abstract"]) for hit in search_results]
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

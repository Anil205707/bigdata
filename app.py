from flask import Flask, render_template, request
from whoosh.qparser import QueryParser
from whoosh.index import open_dir

app = Flask(__name__)
index = open_dir("search_index")

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        query = request.form["query"]
        with index.searcher() as searcher:
            parser = QueryParser("abstract", index.schema)
            myquery = parser.parse(query)
            search_results = searcher.search(myquery, limit=10)
            # Copy necessary data before closing the searcher
            results = [
                {"title": hit["title"], "abstract": hit["abstract"]}
                for hit in search_results
            ]
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

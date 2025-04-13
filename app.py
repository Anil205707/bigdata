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
            results = []
            for hit in search_results:
                title = hit.get("title", "No title")
                abstract = hit.get("abstract", "No abstract available")
                results.append({"title": title, "abstract": abstract})
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

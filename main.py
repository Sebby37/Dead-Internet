import flask
from urllib.parse import urlparse

from ReaperEngine import *

app = flask.Flask(__name__)
engine = ReaperEngine()

@app.route("/", defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # Handle search and no seach
    query = flask.request.args.get("query")
    if not query and not path:
        return engine.get_index()
    if query and not path:
        return engine.get_search(query)
    if path == "_export":
        return engine.export_internet()
    
    # Generate the page
    parsed_path = urlparse("http://" + path)
    generated_page = engine.get_page(parsed_path.netloc, path=parsed_path.path)
    return generated_page

if __name__ == "__main__":
    app.run()
    print(engine.export_internet())

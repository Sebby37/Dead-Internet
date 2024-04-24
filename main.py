import flask
import webbrowser
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
    # Use threading to open the browser a bit after the server starts
    from threading import Timer
    def open_browser():
        webbrowser.open("http://127.0.0.1:5000")
    Timer(1, open_browser).start()  # Wait 1 second for the server to start

    app.run(use_reloader=False)  # Disable the reloader if it interferes with opening the browser
    print(engine.export_internet())

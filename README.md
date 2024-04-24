# Dead-Internet
So we all know the classic [Dead Internet Theory](https://en.wikipedia.org/wiki/Dead_Internet_theory), and if you're reading this I assume you at least know what an LLM is. Need I say much more? Yeah of course!

This is a little project I threw together in a couple hours that lets you surf a completely fake web! You run a search query in the only non-generated page `/` and it generates a search results page with fake links that lead to fake websites that lead to more fake websites! 
It's not perfect, not by a long shot, but it works well enough for me to spend like an hour just going through it and laughing at what it makes.

## How do I run this???
Simple, first install Ollama [here](https://ollama.com/download), then pull your model of choice. The one I used is [Llama 3 8B Instruct](https://ollama.com/library/llama3) which works really well and is very impressive for an 8B model.

Next you'll need to install Python if you don't already have it, I run Python 3.10.12 (came with my Linux Mint install), then the libraries you'll need are:
- [OpenAI](https://pypi.org/project/openai/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [Flask](https://pypi.org/project/Flask/)

Once those are installed, simply run the main.py file and navigate to http://127.0.0.1:5000 or whatever URL Flask gives you and have fun!

If you encounter any issues with the search results page, reload and it'll generate a new page. If you get any issues with the other generated pages then try make slight adjustments to the URL to get a different page, right now there isn't yet a way to regenerate a page.

Also when you navigate to the `/_export` path or kill the server, the JSON of your current internet will be saved to the file `internet.json` in the root of the project. Right now you can't load it back yet but maybe I'll add that in the future if I want, or you could fork it and add it yourself the code isn't very complicated at all.

import os
import json
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv

''' About the name...
I apologise for it sounding pretentious or whatever, but I dont care it sounds cool and cyberpunk-y(-ish)
and fits with the Dead Internet Theory theme of this little project
'''

load_dotenv()

class ReaperEngine:
    def __init__(self):
        self.client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY")) # Ollama is pretty cool
        self.internet_db = dict() # TODO: Exporting this sounds like a good idea, losing all your pages when you kill the script kinda sucks ngl, also loading it is a thing too

        self.temperature = 2.1 # Crank up for goofier webpages (but probably less functional javascript)
        self.max_tokens = 4096
        self.system_prompt = "You are an expert in creating realistic webpages. You do not create sample pages, instead you create webpages that are completely realistic and look as if they really existed on the web. You do not respond with anything but HTML, starting your messages with <!DOCTYPE html> and ending them with </html>. If a requested page is not a HTML document, for example a CSS or Javascript file, write that language instead of writing any HTML. If the requested page is instead an image file or other non-text resource, attempt to generate an appropriate resource for it instead of writing any HTML. You use very little to no images at all in your HTML, CSS or JS."
    
    def _sanitize_links(self, dirty_html):
        # Teensy function to replace all links on the page so they link to the root of the server
        # Also to get rid of any http(s), this'll help make the link database more consistent
        
        soup = BeautifulSoup(dirty_html, "html.parser")
        for a in soup.find_all("a"):
            print(a["href"])
            if "mailto:" in a["href"]:
                continue
            a["href"] = a["href"].replace("http://", "")
            a["href"] = a["href"].replace("https://", "")
            a["href"] = "/" + a["href"]
        return str(soup)
    
    def get_index(self):
        # Super basic start page, just to get everything going
        return "<!DOCTYPE html><html><body><h3>Enter the Dead Internet</h3><form action='/' ><input name='query'> <input type='submit' value='Search'></form></body></html>"
    
    def get_page(self, url, path, query=None):
        # Return already generated page if already generated page
        try: return self.internet_db[url][path]
        except: pass
        
        # Construct the basic prompt
        prompt = f"Give me a classic geocities-style webpage from the fictional site of '{url}' at the resource path of '{path}'. Make sure all links generated either link to an external website, or if they link to another resource on the current website have the current url prepended ({url}) to them. For example if a link on the page has the href of 'help' or '/help', it should be replaced with '{url}/path'."
        # TODO: I wanna add all other pages to the prompt so the next pages generated resemble them, but since Llama 3 is only 8k context I hesitate to do so

        # Add other pages to the prompt if they exist
        if url in self.internet_db and len(self.internet_db[url]) > 1:
            pass
        
        # Generate the page
        generated_page_completion = self.client.chat.completions.create(messages=[
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }],
            model="llama3", # What a great model, works near perfectly with this, shame its only got 8k context (does Ollama even set it to that by default?)
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        # Add the page to the database
        generated_page = generated_page_completion.choices[0].message.content
        if not url in self.internet_db:
            self.internet_db[url] = dict()
        self.internet_db[url][path] = self._sanitize_links(generated_page)

        open("curpage.html", "w+").write(generated_page)
        return self._sanitize_links(generated_page)
    
    def get_search(self, query):
        # Generates a cool little search page, this differs in literally every search and is not cached so be weary of losing links
        search_page_completion = self.client.chat.completions.create(messages=[
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": f"Generate the search results page for a ficticious search engine where the search query is '{query}'. Please include at least 10 results to different ficticious websites that relate to the query. DO NOT link to any real websites, every link should lead to a ficticious website. Feel free to add a bit of CSS to make the page look nice. Each search result will link to its own unique website that has nothing to do with the search engine. Make sure each ficticious website has a unique and somewhat creative URL. Don't mention that the results are ficticious."
            }],
            model="llama3",
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        return self._sanitize_links(search_page_completion.choices[0].message.content)

    def export_internet(self, filename="internet.json"):
        json.dump(self.internet_db, open(filename, "w+"))
        russells  = "Russell: I'm reading it here on my computer. I downloaded the internet before the war.\n"
        russells += "Alyx: You downloaded the entire internet.\n"
        russells += "Russell: Ehh, most of it.\n"
        russells += "Alyx: Nice.\n"
        russells += "Russell: Yeah, yeah it is."
        return russells

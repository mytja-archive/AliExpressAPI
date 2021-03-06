from bs4 import BeautifulSoup
import requests
import json

class AliExpressAPI:
    def get(self, url):
        return requests.get(url).text
    
    def search(self, keyword):
        # Get URL
        url = "https://aliexpress.com/wholesale?SearchText="+keyword

        # BS4
        soup = BeautifulSoup(self.get(url), 'html.parser')
        div = soup.find_all("script", type="text/javascript")

        # Convert
        script = div
        for s in script:
            s = str(s)
            if ('window.runParams = {"mods"' in s):
                script = s.split(";")
                for s in script:
                    if ('window.runParams = {"mods"' in s):
                        script = s.replace("window.runParams = ", "")

                        # Validate links
                        script = script.replace("http://aliexpress.com", "//aliexpress.com")
                        script = script.replace("https://aliexpress.com", "//aliexpress.com")
                        script = script.replace("//aliexpress.com", "https://aliexpress.com")
                        script = script.replace("http://ae01.alicdn.com", "//ae01.alicdn.com")
                        script = script.replace("//ae01.alicdn.com", "https://aliexpress.com")

                        # Return JSON
                        return json.loads(script)
        
        raise Exception("Nothing is found")
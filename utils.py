from cookies import cookies
from headers import headers
from params import params

from htmlement import fromstring as parseHTML

class sharedData:
    def __init__(self, debugInfo=False):
        self.debugInfo = debugInfo
        self.searchHeaders = headers
        self.searchParams = params
        self.searchCookies = cookies
        
    def parseHTMLForSearchResults(self, htmlText, query):
        self.htmlParsed = parseHTML(htmlText)
        searchResultsParsed = {
            'results': [],
        }
        loweredQuery = query.lower()

        for element in self.htmlParsed.iter('a'):
            link = element.attrib['href']
            text = element.text

            if not text:
                continue

            try:
                int(text)
                continue
            except:
                pass

            loweredText = text.lower()

            if loweredQuery not in loweredText:
                continue

            link = f'https://iptorrents.com{link}'

            if '/t/' in link:
                if self.debugInfo:
                    print(f'Found: {text} - {link}')

                searchResultsParsed['results'].append(
                    {
                        'torrentName': text,
                        'torrentLink': link,
                    }
                )

        if len(searchResultsParsed['results']) != 0:
            return searchResultsParsed

        if self.debugInfo:
            print(f'No results found for: {query}')

        return False
    
if __name__ == "__main__":
    print('Do not run me')
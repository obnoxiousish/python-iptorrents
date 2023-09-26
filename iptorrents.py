import httpx

from utils import sharedData

class IPTorrents:
    def __init__(self, beAsync=True, debugInfo=False):
        self.sharedData = sharedData(debugInfo=debugInfo)
        self.beAsync = beAsync
        
        if self.beAsync:
            self.session = httpx.AsyncClient(
                headers=self.sharedData.searchHeaders,
                cookies=self.sharedData.searchCookies
            )
        else:
            self.session = httpx.Client(
                headers=self.sharedData.searchHeaders,
                cookies=self.sharedData.searchCookies
            )
        
    async def asyncSearch(self, query, **kwargs):
        searchParams = self.sharedData.searchParams
        searchParams['q'] = query
        
        searchParams.update(kwargs)
        
        searchResults = await self.session.get(
            'https://iptorrents.com/t#torrents',
            params=searchParams,
        )
        
        return self.sharedData.parseHTMLForSearchResults(searchResults.text, query)
    
    def search(self, query, **kwargs):
        searchParams = self.sharedData.searchParams
        searchParams['q'] = query
        
        searchParams.update(kwargs)
        
        searchResults = self.session.get(
            'https://iptorrents.com/t#torrents',
            params=searchParams,
        )
        
        return self.sharedData.parseHTMLForSearchResults(searchResults.text, query)
    
if __name__ == "__main__":
    instance = IPTorrents(beAsync=False, debugInfo=True)
    searchResults = instance.search(
        "oppenheimer",
        o="seeders",
    )
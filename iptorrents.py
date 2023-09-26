from httpx import AsyncClient
from httpx import Client

from os import makedirs
from os import path

from utils import sharedData

class IPTorrents:
    def __init__(self, beAsync=True, debugInfo=False):
        self.sharedData = sharedData(debugInfo=debugInfo)
        self.beAsync = beAsync
        
        self.debugInfo = debugInfo
        
        if self.beAsync:
            self.session = AsyncClient(
                headers=self.sharedData.searchHeaders,
                cookies=self.sharedData.searchCookies
            )
        else:
            self.session = Client(
                headers=self.sharedData.searchHeaders,
                cookies=self.sharedData.searchCookies
            )
        
    async def asyncSearch(self, query, **kwargs):
        if not self.beAsync:
            raise ValueError("This function can only be used with asynchronous mode.")
        
        searchParams = self.sharedData.searchParams
        searchParams['q'] = query
        
        searchParams.update(kwargs)
        
        searchResults = await self.session.get(
            'https://iptorrents.com/t#torrents',
            params=searchParams,
        )
        
        return self.sharedData.parseHTMLForSearchResults(searchResults.text, query)
    
    def search(self, query, **kwargs):
        if self.beAsync:
            raise ValueError("This function can't be used in asynchronous mode.")
        
        searchParams = self.sharedData.searchParams
        searchParams['q'] = query
        
        searchParams.update(kwargs)
        
        searchResults = self.session.get(
            'https://iptorrents.com/t#torrents',
            params=searchParams,
        )
        
        return self.sharedData.parseHTMLForSearchResults(searchResults.text, query)

    async def asyncDownloadTorrent(self, torrentLink, directory='.'):
        if not self.beAsync:
            raise ValueError("This function can only be used with asynchronous mode.")
        
        async with self.session.stream("GET", torrentLink) as response:
            # Ensure the request was successful and the content type is expected
            if response.status_code == 200 and 'application/x-bittorrent' in response.headers.get('content-type', ''):
                return await self._asyncDownloadTorrent(directory, torrentLink, response)
            else:
                return "Failed to download the torrent."
            
    async def _asyncDownloadTorrent(self, directory, torrentLink, response):
        filename = path.join(directory, torrentLink.split("/")[-1])  # Assuming the torrent name is the last part of the URL
        
        # Ensure the directory exists
        makedirs(path.dirname(filename), exist_ok=True)
        
        # Save the torrent file
        with open(filename, 'wb') as torrentFile:
            async for chunk in response.aiter_bytes():
                torrentFile.write(chunk)
        
        returnString = f"Torrent downloaded and saved as {filename}"
        
        if self.debugInfo:
            print(returnString)
        
        return returnString

    def downloadTorrent(self, torrentLink, directory='.'):
        if self.beAsync:
            raise ValueError("This function can't be used in asynchronous mode.")

        if self.debugInfo:
            print(f'Downloading torrent: {torrentLink}')

        with self.session.stream("GET", torrentLink) as response:
            # Ensure the request was successful and the content type is expected
            if self.debugInfo:
                print(f'Content type: {response.headers.get("content-type", "")}')
            return self._downloadTorrent(directory, torrentLink, response)

    def _downloadTorrent(self, directory, torrentLink, response):
        filename = path.join(directory, torrentLink.split("/")[-1])  # Assuming the torrent name is the last part of the URL

        # Ensure the directory exists
        if self.debugInfo:
            print(f'Ensuring directory exists: {path.dirname(filename)}')
            
        makedirs(path.dirname(filename), exist_ok=True)

        # Save the torrent file
        with open(filename, 'wb') as torrentFile:
            for chunk in response.iter_bytes():
                torrentFile.write(chunk)

        returnString = f"Torrent downloaded and saved as {filename}"

        if self.debugInfo:
            print(returnString)

        return returnString

    
if __name__ == "__main__":
    instance = IPTorrents(beAsync=False, debugInfo=True)
    searchResults = instance.search(
        "oppenheimer",
        o="seeders",
    )
    instance.downloadTorrent(
        torrentLink=searchResults['results'][0]['dotTorrentDownloadLink'],
        directory='.',
    )
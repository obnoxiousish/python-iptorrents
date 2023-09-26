# python-iptorrents
a iptorrents search scraper + download .torrent

make sure to replace cookies in cookies.py

```
instance = IPTorrents(beAsync=False, debugInfo=True)
searchResults = instance.search(
    "oppenheimer",
    o="seeders",
)
```
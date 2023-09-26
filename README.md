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

also

```
instance = IPTorrents(beAsync=True, debugInfo=True)
await searchResults = instance.asyncSearch(
    "oppenheimer"
    o="seeders",
)
```

should work with asyncio and trio, and i imagine anyio and curio idk for sure tho, didnt even test it
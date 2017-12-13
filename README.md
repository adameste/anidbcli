# pyAnidbClient
## AniDB UDP API client written in Python

# Introduction
This client is developed, because of missing AniDB clients for multiplatform CLI. This is useful when your anime collection is on a remote linux NAS storage and you want to add the files to your collection on AniDB servers without downloading them locally. This project is developed for MI-PYT course at Czech Technical University - Faculty of Information Technologies and first release version should be available before 1.2.2018.

# Functions
- ed2k link hashing written in cython ([specification](https://en.wikipedia.org/wiki/Ed2k_URI_scheme))
- uses anidb UDP API ([specification](https://wiki.anidb.net/w/UDP_API_Definition))
- add files to anidb MyList
- rename files using specified rules
- organize files into folders (Watched/Unwatched + name of the anime)
- utilizes multiple processor cores (asyncio)
- project will be published to PyPi (ed2k library may be separated from the client)
- *50 pts not required, just need to pass*

# Used libraries
- click
- cython
- asyncio

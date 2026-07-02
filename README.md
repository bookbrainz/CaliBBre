# CaliBBre
A calibre plugin for Integration with the BookBrainz API
## Features 
### Metadata Tab 
Update metadata for a selected Calibre book.<br>

<img width="783" height="431" alt="harry_potter" src="https://github.com/user-attachments/assets/c1e73632-8a97-4317-b952-2f7640ba12e8" /> <br>

The updated metadata of the book will contain:
-  Name
-  Authors
-  Language
-  Publisher
-  Releasedate
-  Disambiguation
-  Sort Name
-  Identifiers (isbn-10, isbn-13, bbid etc)
-  Cover art from [Open Library](https://openlibrary.org/dev/docs/api/covers)


## Installation

### Option 1: From ZIP
Download the zip file and install it like this (for v.1.0.0):
```bash
calibre-customize -a CaliBBre_v1.0.0.zip
```
### Option 2: From source (clone repo)
Clone the repository and build the plugin:
```bash
git clone https://github.com/bookbrainz/CaliBBre
calibre-customize -b /path/to/CaliBBre
```




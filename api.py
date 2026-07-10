import json
from urllib.parse import urlencode
from urllib.request import urlopen


class BookBrainzAPI:
    """
    Public BookBrainz API
    """

    BASE_URL = "https://api.bookbrainz.org/1"

    @staticmethod
    def search_editions(query, size=10):
        """Returns a list of edition search results matching the given query string"""
        search_url = (
            f"{BookBrainzAPI.BASE_URL}/search?{urlencode({'q': query, 'type': 'edition', 'size': size, 'from': 0})}"
        )
        response = urlopen(search_url, timeout=10)
        search_data = json.loads(response.read().decode("utf-8"))
        return search_data.get("searchResult", [])

    @staticmethod
    def get_edition_details(bbid):
        """Fetches details of a edition by BBID"""
        detail_url = f"{BookBrainzAPI.BASE_URL}/edition/{bbid}"
        response = urlopen(detail_url, timeout=10)
        return json.loads(response.read().decode("utf-8"))

    @staticmethod
    def get_edition_identifiers(bbid):
        """Fetches the list of identifiers for a edition by BBID"""
        url = f"{BookBrainzAPI.BASE_URL}/edition/{bbid}/identifiers"
        response = urlopen(url, timeout=10)
        return json.loads(response.read().decode("utf-8"))

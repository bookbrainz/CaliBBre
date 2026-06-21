import requests


class BookBrainzAPI:
    """
    Public BookBrainz API
    """

    BASE_URL = "https://api.bookbrainz.org/1"

    @staticmethod
    def search_editions(query, size=10):
        """Returns a list of edition search results matching the given query string"""
        search_url = (
            f"{BookBrainzAPI.BASE_URL}/search?q={query}&type=edition&size={size}&from=0"
        )
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        search_data = response.json()
        return search_data.get("searchResult", [])

    @staticmethod
    def get_edition_details(bbid):
        """Fetches details of a edition by BBID"""
        detail_url = f"{BookBrainzAPI.BASE_URL}/edition/{bbid}"
        response = requests.get(detail_url, timeout=10)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_edition_identifiers(bbid):
        """Fetches the list of identifiers for a edition by BBID"""
        url = f"{BookBrainzAPI.BASE_URL}/edition/{bbid}/identifiers"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

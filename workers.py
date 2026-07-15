from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from qt.core import QThread, pyqtSignal

from .api import BookBrainzAPI


class BookSearchWorker(QThread):
    """Searches BookBrainz editions by the selected Calibre book's title"""

    results_found = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, search_query):
        super().__init__()
        self.search_query = search_query

    def run(self):
        try:
            results = BookBrainzAPI.search_editions(self.search_query)
            self.results_found.emit(results)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()


class BookSearchByNameWorker(QThread):
    """Background worker for text searches on the Browse tab"""

    results_found = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, search_query):
        super().__init__()
        self.search_query = search_query

    def run(self):
        try:
            results = BookBrainzAPI.search_editions(self.search_query)
            self.results_found.emit(results)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()


class GetEditionDetailsByBBID(QThread):
    """Fetches the full edition record, identifiers, and cover art for a specific BBID"""

    edition_data_fetched = pyqtSignal(dict)
    identifiers_fetched = pyqtSignal(dict)
    cover_fetched = pyqtSignal(object)
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, bbid):
        super().__init__()
        self.bbid = bbid

    def run(self):
        identifiers_result = {}
        errors = []

        with ThreadPoolExecutor(max_workers=2) as executor:
            metadata_details = executor.submit(
                BookBrainzAPI.get_edition_details, self.bbid
            )
            edition_identifiers = executor.submit(
                BookBrainzAPI.get_edition_identifiers, self.bbid
            )

            for fetched_data in as_completed([metadata_details, edition_identifiers]):
                if fetched_data is metadata_details:
                    try:
                        edition_data_result = fetched_data.result()
                        self.edition_data_fetched.emit(edition_data_result)
                    except Exception as e:
                        errors.append(str(e))
                elif fetched_data is edition_identifiers:
                    try:
                        identifiers_result = fetched_data.result()
                        self.identifiers_fetched.emit(identifiers_result)
                    except Exception as e:
                        errors.append(str(e))

        if errors:
            self.error_occurred.emit(errors[0])
            self.finished.emit()
            return

        try:
            isbn = None
            for id_item in identifiers_result.get("identifiers", []):
                if id_item.get("type", "").lower() in ["isbn-10", "isbn-13"]:
                    isbn = id_item.get("value")
                    break

            cover_bytes = None
            if isbn:
                cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
                resp = requests.get(cover_url, timeout=10)
                if resp.status_code == 200:
                    cover_bytes = resp.content
            self.cover_fetched.emit(cover_bytes)
        except Exception:
            self.cover_fetched.emit(None)

        self.finished.emit()

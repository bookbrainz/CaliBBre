from calibre.utils.localization import calibre_langcode_to_name

def language_name(code, localize=True):

    if not code:
        return code
    return calibre_langcode_to_name(code, localize=localize)

def format_languages(lang_codes, default="Unknown", localize=True):
    """Return a comma-joined string of language names from ISO language codes"""

    if not lang_codes:
        return default
    return ", ".join(
        language_name(code, localize=localize) for code in lang_codes
    )

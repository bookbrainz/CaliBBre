from calibre.customize import InterfaceActionBase

class CalibbrePlugin(InterfaceActionBase):
    name = "CaliBBre"
    description = "A plugin for Integration with bookbrainz"
    supported_platforms = ["windows", "osx", "linux"]
    author = "Md Waqib Sk"
    version = (1, 0, 0)
    minimum_calibre_version = (0, 7, 53)

    actual_plugin = "calibre_plugins.calibbre.main:BookBrainzAction"

    def is_customizable(self):
        """ """
        return False

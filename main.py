from calibre.gui2.actions import InterfaceAction

from .plugin import BookBrainzPlugin


class BookBrainzAction(InterfaceAction):
    name = "BookBrainz Plugin"

    action_spec = (
        "BookBrainz Plugin",
        None,
        "Search on BookBrainz",
        None,
    )

    def genesis(self):

        icon = get_icons("images/BookBrainz_logo_icon.svg")
        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)

    def show_dialog(self):
        """
        This runs when the user clicks the toolbar icon
        """
        d = BookBrainzPlugin(self.gui)

        # Show the window and wait for it to close
        d.exec_()

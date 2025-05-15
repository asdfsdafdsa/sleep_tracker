"""
Base screen class for all screens in the application.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class BaseScreen(toga.Box):
    def __init__(self, app):
        """Initialize the base screen.
        
        Args:
            app: The main application instance
        """
        super().__init__(style=Pack(direction=COLUMN, padding=20))
        self.app = app
        
        # Create a header box
        self.header = toga.Box(style=Pack(direction=ROW, padding_bottom=20))
        self.add(self.header)
        
        # Create a content box
        self.content = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.add(self.content)
        
        # Create a footer box
        self.footer = toga.Box(style=Pack(direction=ROW, padding_top=20))
        self.add(self.footer)
    
    def add_header_button(self, text, on_press=None):
        """Add a button to the header.
        
        Args:
            text: The text to display on the button
            on_press: The callback function to call when the button is pressed
        """
        button = toga.Button(text, on_press=on_press, style=Pack(padding=5))
        self.header.add(button)
    
    def add_footer_button(self, text, on_press=None):
        """Add a button to the footer.
        
        Args:
            text: The text to display on the button
            on_press: The callback function to call when the button is pressed
        """
        button = toga.Button(text, on_press=on_press, style=Pack(padding=5))
        self.footer.add(button)
    
    def show_error(self, message):
        """Show an error message to the user.
        
        Args:
            message: The error message to display
        """
        self.app.main_window.error_dialog('Error', message)
    
    def show_info(self, message):
        """Show an info message to the user.
        
        Args:
            message: The info message to display
        """
        self.app.main_window.info_dialog('Information', message) 
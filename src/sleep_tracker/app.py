"""
App for Programming class
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class SleepTracker(toga.App):
    def startup(self):
        """Construct and show the Toga application."""
        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Add user state
        self.current_user = None
        self.user_role = None
        
        # Create a container for the content
        self.content = toga.Box(style=Pack(direction=COLUMN))
        
        # Set the content of the main window
        self.main_window.content = self.content
        
        # Show the main window
        self.main_window.show()
        
        # Initialize the login screen
        self.show_login_screen()
    
    def show_login_screen(self):
        """Show the login screen."""
        from .screens.login_screen import LoginScreen
        screen = LoginScreen(self)
        self.content.clear()
        self.content.add(screen)
    
    def show_main_menu(self):
        """Show the main menu screen."""
        from .screens.main_menu import MainMenuScreen
        screen = MainMenuScreen(self)
        self.content.clear()
        self.content.add(screen)
    
    def show_input_screen(self):
        """Show the input screen."""
        from .screens.input_screen import InputScreen
        screen = InputScreen(self)
        self.content.clear()
        self.content.add(screen)
    
    def show_history_screen(self):
        """Show the history screen."""
        from .screens.history_screen import HistoryScreen
        screen = HistoryScreen(self)
        self.content.clear()
        self.content.add(screen)
    
    def show_report_screen(self):
        """Show the report screen."""
        from .screens.report_screen import ReportScreen
        screen = ReportScreen(self)
        self.content.clear()
        self.content.add(screen)
    
    def show_admin_screen(self):
        """Show the admin screen."""
        from .screens.admin_screen import AdminScreen
        screen = AdminScreen(self)
        self.content.clear()
        self.content.add(screen)

def main():
    return SleepTracker()

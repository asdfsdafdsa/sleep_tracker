"""
Report screen for viewing sleep statistics.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .base_screen import BaseScreen
from datetime import datetime, timedelta
from ..database.supabase_db import fetch_sleep_logs

class ReportScreen(BaseScreen):
    def __init__(self, app):
        """Initialize the report screen.
        
        Args:
            app: The main application instance
        """
        super().__init__(app)
        
        # Create a container for the main content
        main_content = toga.Box(style=Pack(direction=COLUMN, padding=20))
        
        # Add a back button
        back_button = toga.Button(
            'Вернуться в меню',
            on_press=self.go_back,
            style=Pack(padding=5, width=200)
        )
        main_content.add(back_button)
        
        # Create a container for the report
        self.report_container = toga.Box(style=Pack(direction=COLUMN, padding=10))
        main_content.add(self.report_container)
        
        # Add the main content to the screen
        self.content.add(main_content)
        
        # Update the report
        self.update_report()
    
    def update_report(self):
        """Update the report with the latest data."""
        # Clear the report container
        self.report_container.clear()
        
        # Получаем все логи сна из Supabase
        logs = fetch_sleep_logs()
        # Группируем по пользователям
        user_logs = {}
        for log in logs:
            user = log['login']
            user_logs.setdefault(user, []).append(log)
        
        # Display report for each user
        for user, logs in user_logs.items():
            # Add user header
            self.report_container.add(toga.Label(
                f"\nПользователь: {user}",
                style=Pack(font_size=16, padding_bottom=10)
            ))
            
            # Calculate average statistics
            total_sleep_time = 0
            total_wake_time = 0
            total_wellbeing = 0
            days_with_data = len(logs)
            
            for log in logs:
                # Convert time to minutes for calculation
                sleep_time = datetime.strptime(log['sleep_time'], '%H:%M')
                wake_time = datetime.strptime(log['wake_time'], '%H:%M')
                
                # Calculate minutes from start of day
                sleep_minutes = sleep_time.hour * 60 + sleep_time.minute
                wake_minutes = wake_time.hour * 60 + wake_time.minute
                
                total_sleep_time += sleep_minutes
                total_wake_time += wake_minutes
                total_wellbeing += int(log['wellbeing'])
            
            if days_with_data > 0:
                # Calculate averages
                avg_sleep_minutes = total_sleep_time / days_with_data
                avg_wake_minutes = total_wake_time / days_with_data
                avg_wellbeing = total_wellbeing / days_with_data
                
                # Convert minutes back to hours and minutes
                avg_sleep_hour = int(avg_sleep_minutes // 60)
                avg_sleep_min = int(avg_sleep_minutes % 60)
                avg_wake_hour = int(avg_wake_minutes // 60)
                avg_wake_min = int(avg_wake_minutes % 60)
                
                # Format time
                avg_sleep = f"{avg_sleep_hour:02d}:{avg_sleep_min:02d}"
                avg_wake = f"{avg_wake_hour:02d}:{avg_wake_min:02d}"
                
                # Add statistics
                self.report_container.add(toga.Label(
                    f"Среднее время засыпания: {avg_sleep}\n" +
                    f"Среднее время пробуждения: {avg_wake}\n" +
                    f"Среднее самочувствие: {avg_wellbeing:.1f}/10",
                    style=Pack(font_size=14, padding=10)
                ))
    
    def go_back(self, widget):
        """Go back to the main menu."""
        self.app.show_main_menu() 
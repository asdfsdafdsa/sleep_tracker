"""
History screen for viewing sleep data history.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .base_screen import BaseScreen
from datetime import datetime
from ..database.supabase_db import fetch_sleep_logs

class HistoryScreen(BaseScreen):
    def __init__(self, app):
        """Initialize the history screen.
        
        Args:
            app: The main application instance
        """
        super().__init__(app)
        
        # Основной контейнер с flex=1
        main_content = toga.Box(style=Pack(direction=COLUMN, padding=10, flex=1))
        
        # Кнопка возврата на всю ширину
        back_button = toga.Button(
            'Вернуться в меню',
            on_press=self.go_back,
            style=Pack(padding=10)
        )
        main_content.add(back_button)
        
        # Текстовая статистика
        self.stats_label = toga.Label('', style=Pack(padding=10, font_size=15))
        main_content.add(self.stats_label)
        
        self.content.add(main_content)
        self.update_history()
    
    def format_date(self, date_str):
        """Format a date string into a more readable format.
        
        Args:
            date_str: The date string to format
            
        Returns:
            The formatted date string
        """
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        months = {
            1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
            5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
            9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
        }
        return f"{date_obj.day} {months[date_obj.month]} {date_obj.year}г"
    
    def update_history(self):
        """Update the history table with the latest data."""
        if not self.app.current_user:
            return
        
        # Получаем данные из Supabase
        logs = fetch_sleep_logs(login=self.app.current_user)
        if not logs:
            self.stats_label.text = 'Данных нет'
            self.app.main_window.info_dialog('История', 'Данных нет', on_result=lambda _: self.app.show_main_menu())
            return
        # Оставляем только последние 10 дней
        logs = sorted(logs, key=lambda x: x['date'], reverse=True)[:10]
        if not logs:
            self.stats_label.text = 'Данных нет'
            self.app.main_window.info_dialog('История', 'Данных нет', on_result=lambda _: self.app.show_main_menu())
            return
        # Считаем средние значения
        total_sleep = 0
        total_wake = 0
        total_wellbeing = 0
        count = 0
        for log in logs:
            try:
                sleep_h, sleep_m, *_ = map(int, log['sleep_time'].split(':'))
                wake_h, wake_m, *_ = map(int, log['wake_time'].split(':'))
                sleep_minutes = sleep_h * 60 + sleep_m
                wake_minutes = wake_h * 60 + wake_m
                total_sleep += sleep_minutes
                total_wake += wake_minutes
                total_wellbeing += int(log.get('wellbeing', 5))
                count += 1
            except Exception:
                continue
        if count == 0:
            self.stats_label.text = 'Данных нет'
            self.app.main_window.info_dialog('История', 'Данных нет', on_result=lambda _: self.app.show_main_menu())
            return
        avg_sleep = total_sleep // count
        avg_wake = total_wake // count
        avg_wellbeing = total_wellbeing / count
        avg_sleep_str = f"{avg_sleep // 60:02d}:{avg_sleep % 60:02d}"
        avg_wake_str = f"{avg_wake // 60:02d}:{avg_wake % 60:02d}"
        text = (
            f"Статистика за последние 10 дней:\n"
            f"Среднее время сна: {avg_sleep_str}\n"
            f"Среднее время пробуждения: {avg_wake_str}\n"
            f"Среднее самочувствие: {avg_wellbeing:.1f}"
        )
        self.app.main_window.info_dialog('История', text, on_result=lambda _: self.app.show_main_menu())
    
    def go_back(self, widget):
        """Go back to the main menu."""
        self.app.show_main_menu() 
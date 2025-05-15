"""
Admin screen for managing users and viewing system status.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .base_screen import BaseScreen
from ..database.supabase_db import fetch_sleep_logs
from collections import defaultdict

class AdminScreen(BaseScreen):
    def __init__(self, app):
        """Initialize the admin screen.
        
        Args:
            app: The main application instance
        """
        super().__init__(app)
        
        # Проверка прав
        if self.app.user_role != 'admin':
            self.content.add(toga.Label('Доступ запрещен', style=Pack(font_size=18, color='red', padding=20)))
            return
        # Получаем все логи сна
        logs = fetch_sleep_logs()
        if not logs:
            self.content.add(toga.Label('Нет данных для отчета', style=Pack(font_size=16, padding=20)))
            return
        # Группируем по пользователям
        user_logs = defaultdict(list)
        for log in logs:
            user_logs[log.get('login', '???')].append(log)
        # Для каждого пользователя считаем средние значения
        for user, logs in user_logs.items():
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
                continue
            avg_sleep = total_sleep // count
            avg_wake = total_wake // count
            avg_wellbeing = total_wellbeing / count
            avg_sleep_str = f"{avg_sleep // 60:02d}:{avg_sleep % 60:02d}"
            avg_wake_str = f"{avg_wake // 60:02d}:{avg_wake % 60:02d}"
            self.content.add(toga.Label(
                f"Пользователь: {user}\n"
                f"Среднее время сна: {avg_sleep_str}\n"
                f"Среднее время пробуждения: {avg_wake_str}\n"
                f"Среднее самочувствие: {avg_wellbeing:.1f}\n",
                style=Pack(font_size=15, padding=10)
            ))
        
        # Create a container for the main content
        main_content = toga.Box(style=Pack(direction=COLUMN, padding=20))
        
        # Add a back button
        back_button = toga.Button(
            'Вернуться в меню',
            on_press=self.go_back,
            style=Pack(padding=5, width=200)
        )
        main_content.add(back_button)
        
        # Add a label for the admin message
        admin_label = toga.Label(
            'Здесь будет список работников и их состояние.',
            style=Pack(font_size=16, padding=20)
        )
        main_content.add(admin_label)
        
        # Add the main content to the screen
        self.content.add(main_content)
    
    def go_back(self, widget):
        """Go back to the main menu."""
        self.app.show_main_menu() 
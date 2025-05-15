"""
Input screen for entering sleep data.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .base_screen import BaseScreen
from ..database.supabase_db import save_sleep_data, fetch_sleep_logs
from datetime import datetime, date
import asyncio

class InputScreen(BaseScreen):
    def __init__(self, app):
        """Initialize the input screen.
        
        Args:
            app: The main application instance
        """
        super().__init__(app)
        
        # Create a container for the form
        form = toga.Box(style=Pack(direction=COLUMN, padding=20))
        
        # Add a back button
        back_button = toga.Button(
            'Вернуться в меню',
            on_press=self.go_back,
            style=Pack(padding=10)
        )
        form.add(back_button)
        
        # Create sleep time inputs
        sleep_time_box = toga.Box(style=Pack(direction=ROW, padding=5))
        sleep_time_box.add(toga.Label('Время сна:'))
        
        self.sleep_hour = toga.Selection(
            items=[f"{i:02d}" for i in range(24)],
            style=Pack(padding=5, width=100)
        )
        self.sleep_minute = toga.Selection(
            items=[f"{i:02d}" for i in range(60)],
            style=Pack(padding=5, width=100)
        )
        
        sleep_time_box.add(self.sleep_hour)
        sleep_time_box.add(toga.Label(':'))
        sleep_time_box.add(self.sleep_minute)
        form.add(sleep_time_box)
        
        # Create wake time inputs
        wake_time_box = toga.Box(style=Pack(direction=ROW, padding=5))
        wake_time_box.add(toga.Label('Время пробуждения:'))
        
        self.wake_hour = toga.Selection(
            items=[f"{i:02d}" for i in range(24)],
            style=Pack(padding=5, width=100)
        )
        self.wake_minute = toga.Selection(
            items=[f"{i:02d}" for i in range(60)],
            style=Pack(padding=5, width=100)
        )
        
        wake_time_box.add(self.wake_hour)
        wake_time_box.add(toga.Label(':'))
        wake_time_box.add(self.wake_minute)
        form.add(wake_time_box)
        
        # Create wellbeing slider
        wellbeing_box = toga.Box(style=Pack(direction=ROW, padding=5))
        wellbeing_box.add(toga.Label('Оценка самочувствия (1-10):'))
        
        self.wellbeing_selection = toga.Selection(
            items=[str(i) for i in range(1, 11)],
            style=Pack(padding=5, width=100)
        )
        self.wellbeing_selection.value = '5'
        wellbeing_box.add(self.wellbeing_selection)
        
        form.add(wellbeing_box)
        
        # Add submit button
        submit_button = toga.Button(
            'СОХРАНИТЬ',
            on_press=self.save_data,
            style=Pack(padding=10)
        )
        form.add(submit_button)
        
        # Add the form to the content
        self.content.add(form)
    
    async def save_data(self, widget):
        """Save sleep data to database."""
        try:
            # Проверяем, есть ли уже запись за сегодня
            logs = await asyncio.to_thread(fetch_sleep_logs, login=self.app.current_user)
            today_str = date.today().isoformat()
            if any(log.get('date') == today_str for log in logs):
                await self.app.main_window.info_dialog(
                    'Внимание',
                    'Запись за сегодняшний день уже существует. Вы не можете создать две записи за один день.'
                )
                return

            # Получаем значения из полей ввода
            sleep_time = f"{self.sleep_hour.value}:{self.sleep_minute.value}:00"
            wake_time = f"{self.wake_hour.value}:{self.wake_minute.value}:00"
            wellbeing = self.wellbeing_selection.value

            # Сохраняем в базу данных
            await asyncio.to_thread(
                save_sleep_data,
                self.app.current_user,
                sleep_time,
                wake_time,
                wellbeing,
                ''  # пустые заметки
            )

            # Показываем сообщение об успехе
            await self.app.main_window.info_dialog(
                'Успех',
                'Данные успешно сохранены!'
            )

            # Очищаем поля ввода
            self.sleep_hour.value = '00'
            self.sleep_minute.value = '00'
            self.wake_hour.value = '00'
            self.wake_minute.value = '00'
            self.wellbeing_selection.value = '5'

        except Exception as e:
            await self.app.main_window.error_dialog(
                'Ошибка',
                f'Не удалось сохранить данные: {str(e)}'
            )
    
    def go_back(self, widget):
        """Go back to the main menu."""
        self.app.show_main_menu() 
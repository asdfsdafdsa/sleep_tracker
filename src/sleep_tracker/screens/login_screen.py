"""
Login screen for the application.
"""

import toga
import asyncio
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .base_screen import BaseScreen
from ..database.supabase_db import login_user

class LoginScreen(BaseScreen):
    def __init__(self, app):
        """Initialize the login screen.
        
        Args:
            app: The main application instance
        """
        super().__init__(app)
        
        # Create a container for the login form
        form = toga.Box(style=Pack(direction=COLUMN, padding=20, width=350))
        
        # Create the login input
        self.login_input = toga.TextInput(
            placeholder='Логин',
            style=Pack(padding=5, width=300)
        )
        
        # Create the password input
        self.password_input = toga.PasswordInput(
            placeholder='Пароль',
            style=Pack(padding=5, width=300)
        )
        
        # Create the login button
        self.login_button = toga.Button(
            'Войти',
            on_press=lambda w: asyncio.create_task(self.login(w)),
            style=Pack(padding=5, width=300)
        )
        
        # Add widgets to the form
        form.add(self.login_input)
        form.add(self.password_input)
        form.add(self.login_button)
        
        # Картинка и приветствие
        image_box = toga.Box(style=Pack(direction=COLUMN, padding_bottom=10))
        try:
            image = toga.ImageView(toga.Image("assets/sleep_image.png"), style=Pack(width=240, height=240, padding_bottom=10))
            image_box.add(image)
        except Exception:
            image_box.add(toga.Label("[Нет картинки: assets/sleep_image.png]", style=Pack(color='red', font_size=12, padding_bottom=10)))
        image_box.add(toga.Label('Добро пожаловать!', style=Pack(font_size=20, padding_bottom=5)))
        image_box.add(toga.Label('Войдите в приложение.', style=Pack(font_size=14, padding_bottom=15)))
        self.content.add(image_box)
        
        # Add the form to the content
        self.content.add(form)
    
    def show_loading(self, show=True):
        """Show or hide the loading state.
        
        Args:
            show: Whether to show the loading state
        """
        self.login_button.enabled = not show
        self.login_button.text = 'Загрузка...' if show else 'Войти'
    
    def login(self, widget):
        print("НАЖАТИЕ НА ВОЙТИ")
        username = self.login_input.value
        password = self.password_input.value

        if not username or not password:
            self.app.main_window.error_dialog(
                'Ошибка',
                'Пожалуйста, введите имя пользователя и пароль'
            )
            return

        try:
            user = login_user(username, password)
            if user:
                print("УСПЕШНЫЙ ВХОД")
                self.app.current_user = username
                self.app.user_role = user.get('role', 'user')
                self.app.show_main_menu()
            else:
                self.app.main_window.error_dialog(
                    'Ошибка',
                    'Неверное имя пользователя или пароль'
                )
        except Exception as e:
            print("ОШИБКА:", e)
            self.app.main_window.error_dialog(
                'Ошибка',
                f'Не удалось войти: {str(e)}'
            ) 
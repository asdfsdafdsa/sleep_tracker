"""
Main menu screen for the application.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from .base_screen import BaseScreen
import random
import asyncio

# TODO: Move to a separate file
MOTIVATIONAL_PHRASES = [
    "Хороший сон - залог здоровья!",
    "Высыпайтесь и будьте здоровы!",
    "Качественный сон - путь к успеху!",
    "Сладких снов и приятных сновидений!",
    "Здоровый сон - здоровый дух!",
]

class MainMenuScreen(BaseScreen):
    def __init__(self, app):
        """Initialize the main menu screen.
        
        Args:
            app: The main application instance
        """
        super().__init__(app)
        
        main_content = toga.Box(style=Pack(direction=COLUMN, padding_top=40, padding_bottom=40))

        # Картинка по центру
        image_box = toga.Box(style=Pack(direction=COLUMN, alignment="center"))
        try:
            image = toga.ImageView(toga.Image("assets/sleep_image.png"), style=Pack(width=240, height=240, padding_bottom=20))
            image_box.add(image)
        except Exception as e:
            image_box.add(toga.Label("[Нет картинки!]", style=Pack(color='red', font_size=12, padding_bottom=10)))
        main_content.add(image_box)
        
        # Приветствие
        self.greeting_label = toga.Label(
            '',
            style=Pack(font_size=22, padding_bottom=10)
        )
        main_content.add(self.greeting_label)
        
        # Мотивационная фраза
        self.motivational_label = toga.Label(
            '',
            style=Pack(font_size=16, padding_bottom=30)
        )
        main_content.add(self.motivational_label)
        
        #Кнопки на всю ширину
        self.input_button = toga.Button(
            'Ввести данные',
            on_press=self.go_to_input,
            style=Pack(padding=10)
        )
        main_content.add(self.input_button)
        
        self.weekly_button = toga.Button(
            'Еженедельный отчет',
            on_press=self.show_weekly_report,
            style=Pack(padding=10)
        )
        main_content.add(self.weekly_button)
        
        self.tips_button = toga.Button(
            'Советы',
            on_press=lambda w: asyncio.create_task(self.show_tips(w)),
            style=Pack(padding=10)
        )
        main_content.add(self.tips_button)
        
        self.logout_button = toga.Button(
            'Разлогиниться',
            on_press=self.logout,
            style=Pack(padding=10)
        )
        main_content.add(self.logout_button)
        
        self.content.add(main_content)
        self.update_ui()
    
    def update_ui(self):
        """Update the UI based on the current user and role."""
        if self.app.current_user:
            self.greeting_label.text = f"Здравствуйте, {self.app.current_user}!"
            self.motivational_label.text = random.choice(MOTIVATIONAL_PHRASES)
    
    def go_to_input(self, widget):
        """Go to the input screen."""
        self.app.show_input_screen()
    
    def go_to_history(self, widget):
        self.show_history_dialog()

    def show_history_dialog(self):
        from datetime import datetime
        from ..database.supabase_db import fetch_sleep_logs
        logs = fetch_sleep_logs(login=self.app.current_user)
        if not logs:
            self.app.main_window.info_dialog('История', 'Данных нет')
            return
        logs = sorted(logs, key=lambda x: x['date'], reverse=True)[:10]
        if not logs:
            self.app.main_window.info_dialog('История', 'Данных нет')
            return
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
            self.app.main_window.info_dialog('История', 'Данных нет')
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
        self.app.main_window.info_dialog('История', text)
    
    def go_to_report(self, widget):
        self.show_admin_report_dialog()

    def show_admin_report_dialog(self):
        if self.app.user_role != 'admin':
            self.app.main_window.info_dialog('Ошибка', 'Недостаточно прав!')
            return
        from ..database.supabase_db import fetch_sleep_logs
        from collections import defaultdict
        logs = fetch_sleep_logs()
        if not logs:
            self.app.main_window.info_dialog('Отчет', 'Нет данных для отчета')
            return
        user_logs = defaultdict(list)
        for log in logs:
            user_logs[log.get('login', '???')].append(log)
        text = ''
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
            text += (
                f"Пользователь: {user}\n"
                f"Среднее время сна: {avg_sleep_str}\n"
                f"Среднее время пробуждения: {avg_wake_str}\n"
                f"Среднее самочувствие: {avg_wellbeing:.1f}\n\n"
            )
        if not text:
            self.app.main_window.info_dialog('Отчет', 'Нет данных для отчета')
        else:
            self.app.main_window.info_dialog('Отчет', text)
    
    def logout(self, widget):
        """Log out the current user."""
        self.app.current_user = None
        self.app.user_role = None
        self.app.show_login_screen()
    
    async def show_tips(self, widget):
        from datetime import datetime, timedelta
        from ..database.supabase_db import fetch_sleep_logs
        today = datetime.today().date()
        week_ago = today - timedelta(days=6)
        logs = await asyncio.to_thread(fetch_sleep_logs, login=self.app.current_user)
        week_logs = [log for log in logs if 'date' in log and week_ago <= datetime.strptime(log['date'], '%Y-%m-%d').date() <= today]
        if len(week_logs) < 7:
            await self.app.main_window.info_dialog('Совет', 'Недостаточно данных! Вернитесь позднее.')
            return
        # Анализируем средние значения
        total_sleep = 0
        total_wellbeing = 0
        for log in week_logs:
            sleep_time = log.get('sleep_time', '00:00')
            wake_time = log.get('wake_time', '00:00')
            # Время сна в минутах
            try:
                s_h, s_m, *_ = map(int, sleep_time.split(':'))
                w_h, w_m, *_ = map(int, wake_time.split(':'))
                sleep_minutes = (w_h*60 + w_m) - (s_h*60 + s_m)
                if sleep_minutes < 0:
                    sleep_minutes += 24*60
            except Exception:
                sleep_minutes = 0
            total_sleep += sleep_minutes
            try:
                total_wellbeing += int(log.get('wellbeing', 5))
            except Exception:
                total_wellbeing += 5
        avg_sleep = total_sleep / 7 / 60  # в часах
        avg_wellbeing = total_wellbeing / 7
        # Градация советов
        tips = []
        if avg_sleep < 7:
            tips.append('Вы спите меньше рекомендуемой нормы. Недостаток сна может снижать концентрацию, вызывать раздражительность и утомляемость. Постарайтесь ложиться спать на 30–60 минут раньше, избегать экранов перед сном и соблюдать стабильный режим отдыха.')
        elif 7 <= avg_sleep <= 9:
            tips.append('Ваш сон находится в пределах нормы, что отлично сказывается на восстановлении организма, настроении и работоспособности. Продолжайте придерживаться регулярного режима сна даже в выходные дни.')
        else:
            tips.append('Вы, возможно, спите больше, чем нужно. Хотя организму иногда требуется больше времени на восстановление, регулярный избыток сна может быть признаком усталости или отсутствия дневной активности. Попробуйте ложиться и вставать в одно и то же время.')
        if avg_wellbeing < 6:
            tips.append('Ваше самочувствие ниже среднего. Обратите внимание на режим сна, уровень стресса, питание и физическую активность. Постарайтесь включить в день даже короткие прогулки или разминку, это может помочь улучшить общее состояние.')
        elif 6 <= avg_wellbeing <= 8:
            tips.append('Ваше самочувствие в порядке, но всегда есть возможность его улучшить. Продолжайте следить за сном, питанием и уровнем активности. Иногда полезно пробовать новые привычки, такие как дыхательные упражнения или ведение дневника.')
        else:
            tips.append('У вас отличное самочувствие! Это говорит о том, что вы хорошо справляетесь с заботой о себе. Продолжайте поддерживать здоровый образ жизни, сохраняйте баланс между активностью и отдыхом.')
        await self.app.main_window.info_dialog('Совет', '\n'.join(tips))

    def show_weekly_report(self, widget):
        from datetime import datetime, timedelta
        from ..database.supabase_db import fetch_sleep_logs
        from collections import defaultdict
        if self.app.user_role == 'admin':
            # Отчет по всем пользователям за неделю
            logs = fetch_sleep_logs()
            if not logs:
                self.app.main_window.info_dialog('Отчет', 'Нет данных для отчета')
                return
            week_ago = datetime.today().date() - timedelta(days=6)
            user_logs = defaultdict(list)
            for log in logs:
                # Фильтруем только за последнюю неделю
                if 'date' in log:
                    try:
                        log_date = datetime.strptime(log['date'], '%Y-%m-%d').date()
                        if week_ago <= log_date <= datetime.today().date():
                            user_logs[log.get('login', '???')].append(log)
                    except Exception:
                        continue
            text = ''
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
                text += (
                    f"Пользователь: {user}\n"
                    f"Среднее время сна: {avg_sleep_str}\n"
                    f"Среднее время пробуждения: {avg_wake_str}\n"
                    f"Среднее самочувствие: {avg_wellbeing:.1f}\n\n"
                )
            if not text:
                self.app.main_window.info_dialog('Отчет', 'Нет данных для отчета')
            else:
                self.app.main_window.info_dialog('Отчет', text)
        else:
            # Обычный пользователь — статистика за 7 дней
            logs = fetch_sleep_logs(login=self.app.current_user)
            if not logs:
                self.app.main_window.info_dialog('Еженедельный отчет', 'Данных нет')
                return
            logs = sorted(logs, key=lambda x: x['date'], reverse=True)[:7]
            if not logs:
                self.app.main_window.info_dialog('Еженедельный отчет', 'Данных нет')
                return
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
                self.app.main_window.info_dialog('Еженедельный отчет', 'Данных нет')
                return
            avg_sleep = total_sleep // count
            avg_wake = total_wake // count
            avg_wellbeing = total_wellbeing / count
            avg_sleep_str = f"{avg_sleep // 60:02d}:{avg_sleep % 60:02d}"
            avg_wake_str = f"{avg_wake // 60:02d}:{avg_wake % 60:02d}"
            text = (
                f"Статистика за последние 7 дней:\n"
                f"Среднее время сна: {avg_sleep_str}\n"
                f"Среднее время пробуждения: {avg_wake_str}\n"
                f"Среднее самочувствие: {avg_wellbeing:.1f}"
            )
            self.app.main_window.info_dialog('Еженедельный отчет', text) 
import flet as ft
from flet import (
    Page,
    ThemeMode,
    Theme,
    Colors,
    Icons,
    alignment,
    TextAlign,
    FontWeight,
    BoxShadow,
    Offset,
    InputBorder,
    ButtonStyle,
    RoundedRectangleBorder
)

# Основная реализация перенесена в класс AuthPage


class AuthPage:
    def __init__(self):
        self.page = None
        self.username_field = None
        self.password_field = None
        self.confirm_password_field = None  # Поле для подтверждения пароля
        self.email_field = None  # Поле для email
        self.login_button = None
        self.register_button = None  # Кнопка "Зарегистрироваться" для формы входа
        self.confirm_register_button = None  # Кнопка "Подтвердить регистрацию"
        self.switch_mode_button = None  # Кнопка переключения режимов
        self.error_text = None
        self.is_login_mode = True  # Флаг для отслеживания режима (вход/регистрация)

    def main(self, page: ft.Page):
        self.page = page
        page.title = "Авторизация"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.fonts = {
            "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
        }
        page.theme = ft.Theme(font_family="Roboto")
        
        self.create_auth_interface()

    def create_auth_interface(self):
        """Создание интерфейса авторизации/регистрации"""
        # Создание полей ввода
        self.username_field = ft.TextField(
            label="Логин",
            border=ft.InputBorder.UNDERLINE,
            prefix_icon=Icons.PERSON,
            width=300,
            text_size=14
        )

        self.email_field = ft.TextField(
            label="Email",
            border=ft.InputBorder.UNDERLINE,
            prefix_icon=Icons.EMAIL,
            width=300,
            text_size=14,
            visible=False  # Скрыто в режиме входа
        )

        self.password_field = ft.TextField(
            label="Пароль",
            border=ft.InputBorder.UNDERLINE,
            prefix_icon=Icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=300,
            text_size=14
        )

        self.confirm_password_field = ft.TextField(
            label="Подтвердите пароль",
            border=ft.InputBorder.UNDERLINE,
            prefix_icon=Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            width=300,
            text_size=14,
            visible=False  # Скрыто в режиме входа
        )

        self.error_text = ft.Text(
            color=Colors.RED_500,
            size=12,
            visible=False
        )

        # Создание кнопок
        self.login_button = ft.ElevatedButton(
            text="Войти",
            width=300,
            icon=Icons.LOGIN,
            style=ft.ButtonStyle(
                padding=15,
                bgcolor=Colors.BLUE,
                color=Colors.WHITE,
            ),
            on_click=self.handle_login
        )

        # Кнопка регистрации (для формы входа)
        self.register_button = ft.ElevatedButton(
            text="Зарегистрироваться",
            width=300,
            icon=Icons.PERSON_ADD,
            style=ft.ButtonStyle(
                padding=15,
                bgcolor=Colors.BLUE,
                color=Colors.WHITE,
            ),
            on_click=self.handle_register,
            visible=False  # Скрыто в режиме входа
        )

        # Кнопка подтверждения регистрации
        self.confirm_register_button = ft.ElevatedButton(
            text="Подтвердить регистрацию",
            width=300,
            icon=Icons.CHECK_CIRCLE,
            style=ft.ButtonStyle(
                padding=15,
                bgcolor=Colors.GREEN,
                color=Colors.WHITE,
            ),
            on_click=self.handle_register,
            visible=False  # Скрыто в режиме входа
        )

        # Кнопка для переключения между режимами
        self.switch_mode_button = ft.TextButton(
            text="Создать аккаунт",
            icon=Icons.PERSON_ADD,
            on_click=self.switch_mode
        )

        # Создание контейнера с формой
        auth_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Авторизация" if self.is_login_mode else "Регистрация",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),  # Отступ
                    self.username_field,
                    self.email_field,  # Показывается только в режиме регистрации
                    self.password_field,
                    self.confirm_password_field,  # Показывается только в режиме регистрации
                    ft.Container(height=8),  # Отступ
                    self.error_text,
                    ft.Container(height=24),  # Отступ
                    self.login_button,
                    self.register_button,
                    self.confirm_register_button,
                    self.switch_mode_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=40,
            bgcolor=Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=Colors.BLACK26,
                offset=ft.Offset(0, 4)
            )
        )

        # Создание основного контейнера страницы
        main_container = ft.Container(
            content=auth_container,
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=Colors.BLUE_50
        )

        self.page.add(main_container)

    def handle_login(self, e):
        """Обработчик нажатия кнопки входа"""
        username = self.username_field.value
        password = self.password_field.value

        if not username or not password:
            self.error_text.value = "Пожалуйста, заполните все поля"
            self.error_text.visible = True
            self.page.update()
            return

        # Здесь должна быть логика проверки логина и пароля
        # Временная заглушка для демонстрации
        if username == "admin" and password == "admin":
            self.error_text.visible = False
            print("Успешная авторизация")
            # Здесь должен быть код перехода на главную страницу
        else:
            self.error_text.value = "Неверный логин или пароль"
            self.error_text.visible = True
            self.page.update()

    def switch_mode(self, e):
        """Переключение между режимами входа и регистрации"""
        self.is_login_mode = not self.is_login_mode
        
        # Показать/скрыть дополнительные поля
        self.email_field.visible = not self.is_login_mode
        self.confirm_password_field.visible = not self.is_login_mode
        
        # Показать/скрыть кнопки
        self.login_button.visible = self.is_login_mode
        self.register_button.visible = self.is_login_mode  # Кнопка регистрации видна только в режиме входа
        self.confirm_register_button.visible = not self.is_login_mode  # Кнопка подтверждения видна только в режиме регистрации
        
        # Обновить текст и иконку кнопки переключения режимов
        self.switch_mode_button.text = "Создать аккаунт" if self.is_login_mode else "Отмена"
        self.switch_mode_button.icon = Icons.PERSON_ADD if self.is_login_mode else Icons.CLOSE
        
        self.error_text.visible = False
        self.page.update()

    def handle_register(self, e):
        """Обработчик регистрации"""
        username = self.username_field.value
        email = self.email_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value

        # Проверка заполнения всех полей
        if not all([username, email, password, confirm_password]):
            self.error_text.value = "Пожалуйста, заполните все поля"
            self.error_text.visible = True
            self.page.update()
            return

        # Проверка совпадения паролей
        if password != confirm_password:
            self.error_text.value = "Пароли не совпадают"
            self.error_text.visible = True
            self.page.update()
            return

        # Здесь должна быть логика регистрации пользователя
        # Временная заглушка для демонстрации
        print(f"Регистрация пользователя: {username}, {email}")
        self.error_text.visible = False
        self.page.clean()
        self.page.add(ft.Text("Регистрация успешна!"))
        self.page.update()


if __name__ == "__main__":
    auth = AuthPage()
    ft.app(target=auth.main)

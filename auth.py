import flet as ft

def main(page: ft.Page):
    page.title = "Авторизация"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.bgcolor = "#f0f0f0"

    # Текст ошибки (изначально скрыт)
    error_text = ft.Text(
        color="red",
        size=12,
        visible=False
    )

    def login_click(e):
        if not username_field.value or not password_field.value:
            error_text.value = "Пожалуйста, заполните все поля"
            error_text.visible = True
        else:
            # Здесь должна быть проверка логина и пароля
            if username_field.value == "admin" and password_field.value == "admin":
                error_text.visible = False
                page.clean()
                page.add(ft.Text("Успешная авторизация!"))
            else:
                error_text.value = "Неверный логин или пароль"
                error_text.visible = True
        page.update()

    # Создаем поля ввода и кнопку
    username_field = ft.TextField(
        label="Логин",
        width=300,
        bgcolor="white",
    )

    password_field = ft.TextField(
        label="Пароль",
        password=True,
        can_reveal_password=True,
        width=300,
        bgcolor="white",
    )

    login_button = ft.ElevatedButton(
        "Войти",
        width=300,
        style=ft.ButtonStyle(
            padding=15,
        ),
        on_click=login_click,
    )

    # Создаем контейнер с формой
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Авторизация", size=30, weight=ft.FontWeight.BOLD),
                    username_field,
                    password_field,
                    error_text,
                    login_button,
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=400,
            padding=30,
            bgcolor="white",
            border_radius=10,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)


class AuthPage:
    def __init__(self):
        self.page = None
        self.username_field = None
        self.password_field = None
        self.login_button = None
        self.error_text = None

    def main(self, page: Page):
        self.page = page
        page.title = "Авторизация"
        page.theme_mode = ThemeMode.LIGHT
        page.padding = 0
        page.fonts = {
            "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
        }
        page.theme = Theme(font_family="Roboto")
        
        self.create_auth_interface()

    def create_auth_interface(self):
        """Создание интерфейса авторизации"""
        # Создание полей ввода
        self.username_field = ft.TextField(
            label="Логин",
            border=ft.InputBorder.UNDERLINE,
            prefix_icon=ft.icons.PERSON,
            width=300,
            text_size=14
        )

        self.password_field = ft.TextField(
            label="Пароль",
            border=ft.InputBorder.UNDERLINE,
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=300,
            text_size=14
        )

        self.error_text = ft.Text(
            color=ft.colors.RED_400,
            size=12,
            visible=False
        )

        # Создание кнопки входа
        self.login_button = ft.ElevatedButton(
            text="Войти",
            width=300,
            height=40,
            style=ft.ButtonStyle(
                color=ft.WHITE,
                bgcolor=ft.BLUE,
                shape=ft.RoundedRectangleBorder(radius=8)
            ),
            on_click=self.handle_login
        )

        # Создание контейнера с формой
        auth_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Авторизация",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),  # Отступ
                    self.username_field,
                    ft.Container(height=16),  # Отступ
                    self.password_field,
                    ft.Container(height=8),  # Отступ
                    self.error_text,
                    ft.Container(height=24),  # Отступ
                    self.login_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=40,
            bgcolor=ft.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.BLACK12,
                offset=ft.Offset(0, 4)
            )
        )

        # Создание основного контейнера страницы
        main_container = ft.Container(
            content=auth_container,
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.BLUE_50
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


if __name__ == "__main__":
    auth = AuthPage()
    ft.app(target=auth.main)

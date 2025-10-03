import flet as ft
from services.auth_service import AuthService

class AuthView:
    def __init__(self, auth_service: AuthService, on_login_success=None, on_show_register=None, on_show_login=None):
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        self.on_show_register = on_show_register
        self.on_show_login = on_show_login
        self.page = None

    def set_page(self, page):
        """Установка ссылки на страницу для обновления интерфейса"""
        self.page = page

    def show_login(self, e=None):
        """Показать экран входа"""
        if self.on_show_login:
            self.on_show_login()
        else:
            self._show_login_direct()

    def show_register(self, e=None):
        """Показать экран регистрации"""
        if self.on_show_register:
            self.on_show_register()
        else:
            self._show_register_direct()

    def _show_login_direct(self):
        """Прямое отображение экрана входа"""
        if self.page:
            self.page.clean()
            self.page.add(self.create_login_view())
            self.page.update()

    def _show_register_direct(self):
        """Прямое отображение экрана регистрации"""
        if self.page:
            self.page.clean()
            self.page.add(self.create_register_view())
            self.page.update()

    def create_login_view(self):
        """Создание экрана входа"""
        username_field = ft.TextField(
            label="Имя пользователя",
            width=300,
            autofocus=True
        )
        password_field = ft.TextField(
            label="Пароль", 
            password=True,
            width=300
        )
        status_text = ft.Text("", color=ft.Colors.RED)

        async def on_login_click(e):
            username = username_field.value.strip()
            password = password_field.value
            
            if not username or not password:
                status_text.value = "Заполните все поля"
                status_text.color = ft.Colors.RED
                status_text.update()
                return

            success, message = self.auth_service.login(username, password)
            
            if success:
                status_text.value = "Успешный вход!"
                status_text.color = ft.Colors.GREEN
                status_text.update()
                
                # Задержка для отображения сообщения об успехе
                import asyncio
                await asyncio.sleep(0.5)
                
                if self.on_login_success:
                    # Вызываем асинхронный колбэк
                    await self.on_login_success()
            else:
                status_text.value = message
                status_text.color = ft.Colors.RED
                status_text.update()

        return ft.Container(
            content=ft.Column([
                ft.Text("Вход в Культурный гид", 
                       size=28, 
                       weight=ft.FontWeight.BOLD,
                       color=ft.Colors.PRIMARY),
                ft.Container(height=20),
                username_field,
                password_field,
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Войти",
                    on_click=on_login_click,  # Теперь это асинхронная функция
                    width=300,
                    height=45
                ),
                ft.TextButton(
                    "Регистрация", 
                    on_click=self.show_register,
                    width=300
                ),
                status_text
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )

    def create_register_view(self):
        """Создание экрана регистрации"""
        username_field = ft.TextField(
            label="Имя пользователя",
            width=300,
            autofocus=True
        )
        email_field = ft.TextField(
            label='E-mail',
            width=300,
            autofocus=True
        )
        password_field = ft.TextField(
            label="Пароль", 
            password=True,
            width=300
        )
        confirm_password_field = ft.TextField(
            label="Подтвердите пароль", 
            password=True,
            width=300
        )
        status_text = ft.Text("", color=ft.Colors.RED)

        async def on_register_click(e):
            username = username_field.value.strip()
            email = email_field.value.strip()
            password = password_field.value
            confirm_password = confirm_password_field.value

            if not username or not password or not email:
                status_text.value = "Заполните все поля"
                status_text.update()
                return

            if len(username) < 3:
                status_text.value = "Имя пользователя должно быть не менее 3 символов"
                status_text.update()
                return

            if len(password) < 4:
                status_text.value = "Пароль должен быть не менее 4 символов"
                status_text.update()
                return

            if password != confirm_password:
                status_text.value = "Пароли не совпадают"
                status_text.update()
                return

            success, message = self.auth_service.register(username, email, password)
            
            if success:
                status_text.value = "Успешная регистрация! Автоматический вход..."
                status_text.color = ft.Colors.GREEN
                status_text.update()
                
                # Автоматический вход после регистрации
                success_login, message_login = self.auth_service.login(username, password)
                if success_login and self.on_login_success:
                    import asyncio
                    await asyncio.sleep(0.5)
                    await self.on_login_success()
                elif self.on_show_login:
                    status_text.value = "Регистрация успешна! Теперь войдите в систему"
                    status_text.update()
            else:
                status_text.value = message
                status_text.color = ft.Colors.RED
                status_text.update()

        return ft.Container(
            content=ft.Column([
                ft.Text("Регистрация", 
                       size=28, 
                       weight=ft.FontWeight.BOLD,
                       color=ft.Colors.PRIMARY),
                ft.Container(height=20),
                username_field,
                email_field,
                password_field,
                confirm_password_field,
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Зарегистрироваться",
                    on_click=on_register_click,  # Теперь это асинхронная функция
                    width=300,
                    height=45
                ),
                ft.TextButton(
                    "Назад к входу", 
                    on_click=self.show_login,
                    width=300
                ),
                status_text
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )
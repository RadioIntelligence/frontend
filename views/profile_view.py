import flet as ft
from services.auth_service import AuthService
from models.models import UserProfile

class ProfileView:
    def __init__(self, auth_service: AuthService, on_logout=None, on_back=None):
        self.auth_service = auth_service
        self.on_logout = on_logout
        self.on_back = on_back
        self.user_profile = UserProfile()  # Заглушка профиля

    def create_profile_view(self):
        """Создание страницы профиля пользователя"""
        # Заголовок
        header = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=self.on_back,
                    icon_size=24
                ),
                ft.Text(
                    "Мой профиль",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    expand=True,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(width=48)  # для балансировки
            ]),
            padding=ft.padding.symmetric(vertical=12, horizontal=16),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(bottom=ft.BorderSide(color=ft.Colors.GREY_200, width=1))
        )

        # Поля для редактирования профиля
        name_field = ft.TextField(
            label="Имя",
            value=self.user_profile.name,
            width=300
        )
        email_field = ft.TextField(
            label="Email",
            value=self.user_profile.email,
            width=300
        )
        phone_field = ft.TextField(
            label="Телефон",
            value=self.user_profile.phone,
            width=300
        )
        bio_field = ft.TextField(
            label="О себе",
            value=self.user_profile.bio,
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=300
        )

        status_text = ft.Text("", color=ft.Colors.GREEN)
        logout_status_text = ft.Text("", color=ft.Colors.RED)

        def on_save_profile(e):
            """Сохранение профиля"""
            self.user_profile.name = name_field.value
            self.user_profile.email = email_field.value
            self.user_profile.phone = phone_field.value
            self.user_profile.bio = bio_field.value
            
            status_text.value = "Профиль успешно сохранен!"
            status_text.color = ft.Colors.GREEN
            status_text.update()

        def on_logout_click(e):
            """Выход из системы с вызовом метода auth_service"""
            logout_status_text.value = "Выход из системы..."
            logout_status_text.color = ft.Colors.GREY_600
            logout_status_text.update()
            
            # Вызываем метод logout из auth_service
            logout_result = self.auth_service.logout()
            
            if logout_result is True or logout_result is None:
                logout_status_text.value = "Успешный выход из системы"
                logout_status_text.color = ft.Colors.GREEN
                logout_status_text.update()
                
                # Вызываем колбэк после успешного выхода
                if self.on_logout:
                    self.on_logout()
            else:
                logout_status_text.value = "Ошибка при выходе из системы"
                logout_status_text.color = ft.Colors.RED
                logout_status_text.update()

        # Основной контент
        content = ft.Container(
            content=ft.ListView(
                controls=[
                    # Аватар и основная информация
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.ACCOUNT_CIRCLE,
                                    size=80,
                                    color=ft.Colors.PRIMARY
                                ),
                                margin=ft.margin.only(bottom=10)
                            ),
                            ft.Text(
                                self.user_profile.name or "Пользователь",
                                size=18,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                f"Зарегистрирован: {self.user_profile.registration_date}",
                                size=12,
                                color=ft.Colors.GREY_600
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        alignment=ft.alignment.center
                    ),

                    # Форма редактирования
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Редактировать профиль",
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Container(height=10),
                            name_field,
                            email_field,
                            phone_field,
                            bio_field,
                            ft.Container(height=10),
                            ft.ElevatedButton(
                                "Сохранить изменения",
                                on_click=on_save_profile,
                                width=300
                            ),
                            status_text
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=ft.Colors.GREY_50,
                        margin=ft.margin.symmetric(horizontal=16),
                        border_radius=12
                    ),

                    # Статистика
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Статистика",
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Container(height=10),
                            ft.Row([
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(
                                            str(self.user_profile.favorites_count),
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.PRIMARY
                                        ),
                                        ft.Text("Избранное", size=12)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(
                                            str(self.user_profile.visited_count),
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.PRIMARY
                                        ),
                                        ft.Text("Посещено", size=12)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    expand=True
                                ),
                                ft.Container(
                                    content=ft.Column([
                                        ft.Text(
                                            str(self.user_profile.reviews_count),
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.PRIMARY
                                        ),
                                        ft.Text("Отзывы", size=12)
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    expand=True
                                )
                            ])
                        ]),
                        padding=20,
                        margin=ft.margin.symmetric(horizontal=16, vertical=10)
                    ),

                    # Кнопка выхода
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Управление аккаунтом",
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Container(height=10),
                            ft.FilledButton(
                                "Выйти из системы",
                                icon=ft.Icons.LOGOUT,
                                on_click=on_logout_click,
                                width=300,
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.RED
                                )
                            ),
                            logout_status_text
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20
                    ),

                    ft.Container(height=20)
                ],
                padding=0
            ),
            expand=True
        )

        return ft.Column([
            header,
            content
        ])
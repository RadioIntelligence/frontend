# frontend_main.py
# Импорты необходимых библиотек
import flet as ft
import json
import requests  # для отправки HTTP-запросов к API

# === Основной класс приложения ===
class CulturalApp:
    """
    Класс, управляющий логикой и интерфейсом Flet-приложения.
    Содержит методы для отображения экранов, работы с API и аутентификации.
    """
    def __init__(self):
        """
        Инициализация приложения.
        """
        self.page = None  # будет установлено при запуске
        self.map_container = None  # контейнер для карты
        self.recommendations = []  # список достопримечательностей
        self.api_base_url = "http://localhost:8000"  # URL вашего FastAPI-сервера
        self.access_token = None  # токен аутентификации (None, если не вошёл)

    # === Основной метод запуска приложения ===
    def main(self, page: ft.Page):
        """
        Основная точка входа для Flet-приложения.
        Здесь устанавливаются настройки страницы и проверяется аутентификация.
        """
        self.page = page
        # Настройка внешнего вида
        page.title = "Культурный гид"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.fonts = {
            "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
        }
        page.theme = ft.Theme(font_family="Roboto")

        # === Проверка аутентификации ===
        # Если токен уже есть (например, из кэша), сразу показываем основной интерфейс
        # В данном примере токен хранится в памяти Python, но в реальном приложении
        # его можно сохранять в файл, SQLite и т.д.
        if self.access_token:
            self.create_main_interface()
        else:
            # Если токена нет — показываем экран логина
            self.show_login_screen()

    # === Экраны аутентификации ===
    def show_login_screen(self):
        """
        Отображает экран логина.
        Пользователь вводит логин и пароль, затем отправляет запрос на API.
        """
        # Поля ввода
        username_field = ft.TextField(label="Имя пользователя")
        password_field = ft.TextField(label="Пароль", password=True)

        def on_login_click(e):
            """
            Обработчик нажатия на кнопку "Войти".
            Отправляет данные на бэкенд и сохраняет токен при успехе.
            """
            username = username_field.value
            password = password_field.value
            if self.login(username, password):
                # Если логин успешен — очищаем экран и показываем основной интерфейс
                self.page.clean()
                self.create_main_interface()
            else:
                # Иначе — показываем ошибку
                self.page.add(ft.Text("Неверный логин или пароль", color=ft.Colors.RED))

        # Очищаем текущую страницу и добавляем элементы логина
        self.page.clean()
        self.page.add(
            ft.Column([
                ft.Text("Вход", size=24, weight=ft.FontWeight.BOLD),
                username_field,
                password_field,
                ft.ElevatedButton("Войти", on_click=on_login_click),
                # Кнопка "Регистрация" — переход на экран регистрации
                ft.TextButton("Регистрация", on_click=self.show_register_screen)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def show_register_screen(self, e):
        """
        Отображает экран регистрации.
        Пользователь вводит логин и пароль, затем отправляет запрос на API.
        """
        username_field = ft.TextField(label="Имя пользователя")
        password_field = ft.TextField(label="Пароль", password=True)

        def on_register_click(e):
            """
            Обработчик нажатия на кнопку "Зарегистрироваться".
            """
            username = username_field.value
            password = password_field.value
            if self.register(username, password):
                # Если регистрация успешна — показываем сообщение
                self.page.add(ft.Text("Успешно зарегистрированы!", color=ft.Colors.GREEN))
                # После регистрации автоматически логинимся
                if self.login(username, password):
                    self.page.clean()
                    self.create_main_interface()
            else:
                # Иначе — ошибка
                self.page.add(ft.Text("Ошибка регистрации", color=ft.Colors.RED))

        # Очищаем страницу и показываем поля регистрации
        self.page.clean()
        self.page.add(
            ft.Column([
                ft.Text("Регистрация", size=24, weight=ft.FontWeight.BOLD),
                username_field,
                password_field,
                ft.ElevatedButton("Зарегистрироваться", on_click=on_register_click),
                # Кнопка "Назад" — возвращаемся к экрану логина
                ft.TextButton("Назад", on_click=lambda e: self.show_login_screen())
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    # === Методы аутентификации (вызов API) ===
    def login(self, username: str, password: str):
        """
        Отправляет запрос на бэкенд для аутентификации.
        Если успех — сохраняет токен.
        """
        response = requests.post(
            f"{self.api_base_url}/auth/login",
            data={
                "username": username,
                "password": password
            }
        )
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            return True
        return False

    def register(self, username: str, password: str):
        """
        Отправляет запрос на бэкенд для регистрации.
        """
        response = requests.post(
            f"{self.api_base_url}/auth/register",
            json={
                "username": username,
                "password": password
            }
        )
        return response.status_code == 200

    # === Основной интерфейс приложения (после аутентификации) ===
    def load_recommendations(self):
        """
        Загружает список достопримечательностей (в реальном приложении — с API).
        """
        self.recommendations = [
            {
                "id": 1,
                "title": "Исторический музей",
                "type": "Музей",
                "era": "XIX век",
                "distance": "1.2 км",
                "rating": 4.8,
                "image": "🏛️"
            },
            {
                "id": 2,
                "title": "Парк культуры и отдыха",
                "type": "Парк",
                "era": "Современность",
                "distance": "0.8 км",
                "rating": 4.6,
                "image": "🌳"
            },
            {
                "id": 3,
                "title": "Старинная усадьба",
                "type": "Архитектура",
                "era": "XVIII век",
                "distance": "2.1 км",
                "rating": 4.9,
                "image": "🏰"
            },
            {
                "id": 4,
                "title": "Художественная галерея",
                "type": "Галерея",
                "era": "XX век",
                "distance": "1.5 км",
                "rating": 4.7,
                "image": "🖼️"
            }
        ]

    def create_search_bar(self):
        """
        Создаёт строку поиска в заголовке.
        """
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SEARCH, color=ft.Colors.GREY_600),
                ft.TextField(
                    hint_text="Поиск достопримечательностей...",
                    border=ft.InputBorder.NONE,
                    expand=True,
                    text_size=14,
                    on_change=self.on_search_change
                ),
                ft.IconButton(
                    icon=ft.Icons.FILTER_LIST,
                    icon_color=ft.Colors.GREY_600,
                    on_click=self.open_filters
                )
            ]),
            bgcolor=ft.Colors.WHITE,
            border_radius=25,
            padding=ft.padding.symmetric(horizontal=16),
            margin=ft.margin.symmetric(vertical=8),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 2)
            )
        )

    def create_header(self):
        """
        Создаёт заголовок приложения (с логотипом, строкой поиска и профилем).
        """
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(
                        "Культурный гид",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ACCOUNT_CIRCLE,
                        icon_color=ft.Colors.WHITE,
                        on_click=self.open_profile
                    )
                ]),
                self.create_search_bar()
            ]),
            bgcolor=ft.Colors.PRIMARY,
            padding=16,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 2)
            )
        )

    def create_navigation(self):
        """
        Создаёт нижнюю панель навигации.
        """
        nav_items = [
            {"icon": ft.Icons.MAP, "label": "Карта", "active": True},
            {"icon": ft.Icons.EXPLORE, "label": "Каталог"},
            {"icon": ft.Icons.EVENT, "label": "Афиша"},
            {"icon": ft.Icons.FAVORITE, "label": "Избранное"},
            {"icon": ft.Icons.ROUTE, "label": "Маршруты"}
        ]
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.IconButton(
                            icon=item["icon"],
                            icon_color=ft.Colors.WHITE if item.get("active") else ft.Colors.GREY_600,
                            on_click=lambda e, i=index: self.on_nav_click(e, i)
                        ),
                        ft.Text(
                            item["label"],
                            size=10,
                            color=ft.Colors.WHITE if item.get("active") else ft.Colors.GREY_600
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    bgcolor=ft.Colors.PRIMARY if item.get("active") else ft.Colors.TRANSPARENT,
                    border_radius=12,
                    padding=8,
                    margin=2
                ) for index, item in enumerate(nav_items)
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            bgcolor=ft.Colors.WHITE,
            padding=8,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, -2)
            )
        )

    def create_recommendation_card(self, item):
        """
        Создаёт карточку достопримечательности.
        """
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(item["image"], size=24),
                        ft.VerticalDivider(),
                        ft.Column([
                            ft.Text(
                                item["title"],
                                weight=ft.FontWeight.BOLD,
                                size=14
                            ),
                            ft.Row([
                                ft.Container(
                                    content=ft.Text(
                                        item["type"],
                                        size=10,
                                        color=ft.Colors.BLUE_700
                                    ),
                                    bgcolor=ft.Colors.BLUE_50,
                                    border_radius=8,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2)
                                ),
                                ft.Text(
                                    f"⭐ {item['rating']}",
                                    size=10,
                                    color=ft.Colors.AMBER
                                )
                            ], spacing=8)
                        ], expand=True)
                    ]),
                    ft.Row([
                        ft.Text(
                            f"📏 {item['distance']}",
                            size=12,
                            color=ft.Colors.GREY_600
                        ),
                        ft.Text(
                            f"🕒 {item['era']}",
                            size=12,
                            color=ft.Colors.GREY_600
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]),
                padding=12,
                on_click=lambda e: self.open_place_detail(item["id"])
            ),
            elevation=2,
            margin=ft.margin.symmetric(vertical=4),
        )

    def create_recommendations_section(self):
        """
        Создаёт секцию с рекомендациями (список карточек).
        """
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(
                        "Рекомендуем посетить",
                        size=18,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.TextButton(
                        "Все →",
                        on_click=self.open_catalog
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Column([
                    self.create_recommendation_card(item) for item in self.recommendations
                ], scroll=ft.ScrollMode.ADAPTIVE, height=400)
            ]),
            padding=16,
            bgcolor=ft.Colors.GREY_50,
            width=400
        )

    def create_map_section(self):
        """
        Создаёт секцию с картой (в виде заглушки).
        """
        self.map_container = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.MAP, size=48, color=ft.Colors.GREY_400),
                ft.Text(
                    "Карта достопримечательностей",
                    size=16,
                    color=ft.Colors.GREY_600
                ),
                ft.FilledButton(
                    "Открыть карту",
                    icon=ft.Icons.OPEN_IN_FULL,
                    on_click=self.open_full_map
                )
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.GREY_100,
            alignment=ft.alignment.center,
            expand=True,
            on_click=self.open_full_map
        )
        return self.map_container

    def create_main_interface(self):
        """
        Создаёт основной интерфейс приложения: заголовок, карту, рекомендации, навигацию.
        """
        self.load_recommendations()
        main_content = ft.Row([
            ft.Container(
                content=self.create_map_section(),
                expand=True
            ),
            self.create_recommendations_section()
        ], expand=True)
        self.page.clean()  # очищаем предыдущий интерфейс
        self.page.add(
            ft.Column([
                self.create_header(),
                main_content,
                self.create_navigation()
            ], expand=True)
        )

    # === Обработчики событий ===
    def on_search_change(self, e):
        print(f"Поиск: {e.control.value}")

    def open_filters(self, e):
        print("Открытие фильтров")

    def open_profile(self, e):
        print("Открытие профиля")

    def on_nav_click(self, e, index):
        print(f"Навигация: {index}")
        self.update_navigation_state(index)

    def update_navigation_state(self, active_index):
        print(f"Активирована вкладка: {active_index}")

    def open_place_detail(self, place_id):
        print(f"Открытие места: {place_id}")

    def open_catalog(self, e):
        print("Открытие каталога")

    def open_full_map(self, e):
        print("Открытие полной карты")
        # Имитация инициализации карты (в реальности — через WebView или Leaflet)
        map_api = self.initialize_map("map-container", {"center": [52.970756, 36.064358], "zoom": 12})
        # Пример добавления маркеров
        map_api['add_marker'](52.962197, 36.064894, "Памятник Н. С. Лескову")
        map_api['add_marker'](52.961665, 36.065917, "Памятник А. П. Ермолову")
        map_api['add_marker'](52.967952, 36.064322, "Академический театр им. И.С. Тургенева")
        map_api['add_marker'](52.956389, 36.055278, "Гостиный Двор")
        map_api['add_marker'](52.96188, 36.06356, "Собор Михаила Архангела")
        # Установка центра карты
        map_api['set_center'](52.970756, 36.064358)

    # === Python-аналоги JS-функций (заглушки) ===
    def initialize_map(self, container_id, options=None):
        """
        Имитация инициализации карты.
        В реальном приложении — интеграция с Leaflet, Google Maps и т.д.
        """
        print(f'Initializing map in: {container_id}')
        return {
            'add_marker': self.add_marker,
            'set_center': self.set_center
        }

    def add_marker(self, lat, lng, title):
        print(f'Adding marker: {lat}, {lng}, {title}')

    def set_center(self, lat, lng):
        print(f'Setting center: {lat}, {lng}')

    # === Асинхронные методы для запросов к API ===
    async def fetch_recommendations(self):
        """
        Асинхронный запрос к API за рекомендациями.
        Использует токен аутентификации, если он есть.
        """
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        try:
            response = requests.get(f"{self.api_base_url}/recommendations", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'Error fetching recommendations: {e}')
            return []

    async def search_places(self, query, filters=None):
        """
        Асинхронный запрос к API для поиска мест.
        """
        try:
            payload = {"query": query, "filters": filters or {}}
            response = requests.post(f"{self.api_base_url}/search", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'Error searching places: {e}')
            return []

# === Запуск приложения ===
if __name__ == "__main__":
    app = CulturalApp()
    ft.app(target=app.main)

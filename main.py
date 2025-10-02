import flet as ft
import json
import requests  # для запросов к API

class CulturalApp:
    def __init__(self):
        self.page = None
        self.map_container = None
        self.recommendations = []
        self.api_base_url = "http://localhost:8000"  # URL твоего FastAPI
        self.access_token = None  # <-- НОВОЕ

    def login(self, username: str, password: str):
        """Отправка запроса на логин"""
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

    def fetch_recommendations(self):
        """Запрос к защищённому эндпоинту"""
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

    def main(self, page: ft.Page):
        self.page = page
        page.title = "Культурный гид"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.fonts = {
            "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
        }
        page.theme = ft.Theme(font_family="Roboto")

        # Инициализация данных
        self.load_recommendations()

        # Создание интерфейса
        self.create_main_interface()

    def load_recommendations(self):
        """Загрузка рекомендаций"""
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
        """Создание поисковой строки"""
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
        """Создание заголовка"""
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
        """Создание навигации"""
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
        """Создание карточки рекомендации"""
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
        """Создание секции рекомендаций"""
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
        """Создание секции карты"""
        # Заглушка для карты - в реальном приложении здесь будет интеграция с картографическим API
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
        """Создание основного интерфейса"""
        main_content = ft.Row([
            # Карта
            ft.Container(
                content=self.create_map_section(),
                expand=True
            ),
            # Рекомендации
            self.create_recommendations_section()
        ], expand=True)

        self.page.add(
            ft.Column([
                self.create_header(),
                main_content,
                self.create_navigation()
            ], expand=True)
        )

    # Обработчики событий
    def on_search_change(self, e):
        """Обработчик изменения поиска"""
        print(f"Поиск: {e.control.value}")

    def open_filters(self, e):
        """Открытие фильтров"""
        print("Открытие фильтров")

    def open_profile(self, e):
        """Открытие профиля"""
        print("Открытие профиля")

    def on_nav_click(self, e, index):
        """Обработчик клика по навигации"""
        print(f"Навигация: {index}")
        # Обновляем активное состояние кнопок
        self.update_navigation_state(index)

    def update_navigation_state(self, active_index):
        """Обновление состояния навигации"""
        # В реальном приложении здесь будет логика переключения между экранами
        print(f"Активирована вкладка: {active_index}")

    def open_place_detail(self, place_id):
        """Открытие деталей места"""
        print(f"Открытие места: {place_id}")

    def open_catalog(self, e):
        """Открытие каталога"""
        print("Открытие каталога")

    def open_full_map(self, e):
        """Открытие полной карты"""
        print("Открытие полной карты")
        # Инициализация карты
        map_api = self.initialize_map("map-container", {"center": [52.970756, 36.064358], "zoom": 12}) # МЕТКА ЦЕНТРА ОРЛА
        # Пример добавления маркера
        
        map_api['add_marker'](52.962197, 36.064894, "Памятник Н. С. Лескову")
        map_api['add_marker'](52.961665, 36.065917, "Памятник А. П. Ермолову")
        map_api['add_marker'](52.967952, 36.064322, " Академический театр им. И.С. Тургенева")
        map_api['add_marker'](52.956389, 36.055278, "Гостиный Двор")
        map_api['add_marker'](52.96188, 36.06356, "Собор Михаила Архангела")
        
        # ЦЕНТРАЛЬНЫЙ МАРКЕР 
        
        map_api['set_center'](52.970756, 36.064358)


  # --- Добавим Python-аналоги JS-функций ---
    def initialize_map(self, container_id, options=None):
        """
        Инициализация карты (пока просто заглушка)
        В реальности тут будет интеграция с картой (WebView, Leaflet, и т.д.)
        """
        print(f'Initializing map in: {container_id}')
        return {
            'add_marker': self.add_marker,
            'set_center': self.set_center
        }

    def add_marker(self, lat, lng, title):
        print(f'Adding marker: {lat}, {lng}, {title}')
        # Здесь в будущем можно обновлять UI или отправлять в API

    def set_center(self, lat, lng):
        print(f'Setting center: {lat}, {lng}')

    async def fetch_recommendations(self):
        """
        Асинхронный запрос к API за рекомендациями
        """
        try:
            response = requests.get(f"{self.api_base_url}/recommendations")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'Error fetching recommendations: {e}')
            return []

    async def search_places(self, query, filters=None):
        """
        Асинхронный запрос к API для поиска мест
        """
        try:
            payload = {"query": query, "filters": filters or {}}
            response = requests.post(f"{self.api_base_url}/search", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'Error searching places: {e}')
            return []


# JavaScript функции для интеграции (для будущего использования)
js_functions = """
// Функции для работы с картами
function initializeMap(containerId, options) {
    // Инициализация карты
    console.log('Initializing map in:', containerId);
    return {
        addMarker: function(lat, lng, title) {
            console.log('Adding marker:', lat, lng, title);
        },
        setCenter: function(lat, lng) {
            console.log('Setting center:', lat, lng);
        }
    };
}

// Функции для работы с API
async function fetchRecommendations() {
    try {
        const response = await fetch('/api/recommendations');
        return await response.json();
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        return [];
    }
}

async function searchPlaces(query, filters) {
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, filters })
        });
        return await response.json();
    } catch (error) {
        console.error('Error searching places:', error);
        return [];
    }
}
"""

# Запуск приложения
if __name__ == "__main__":
    app = CulturalApp()

    ft.app(target=app.main)

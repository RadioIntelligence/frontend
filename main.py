import flet as ft
import json


class CulturalApp:
    def __init__(self):
        self.page = None
        self.map_container = None
        self.recommendations = []
        self.events = []
        self.current_view = "main"  # "main", "events", "event_detail"
        self.current_event = None

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
        self.load_events()  # <-- добавлено

        # Создание интерфейса
        self.create_main_interface()

    def load_recommendations(self):
        """Загрузка рекомендаций с координатами"""
        self.recommendations = [
            {
                "id": 1,
                "title": "Исторический музей",
                "type": "Музей",
                "era": "XIX век",
                "distance": "1.2 км",
                "rating": 4.8,
                "image": "🏛️",
                "lat": 52.6338,
                "lng": 54.1928
            },
            {
                "id": 2,
                "title": "Парк культуры и отдыха",
                "type": "Парк",
                "era": "Современность",
                "distance": "0.8 км",
                "rating": 4.7,
                "image": "🌳",
                "lat": 52.6300,
                "lng": 54.1950
            },
            {
                "id": 3,
                "title": "Старинная усадьба",
                "type": "Архитектура",
                "era": "XVIII век",
                "distance": "2.1 км",
                "rating": 4.9,
                "image": "🏰",
                "lat": 52.6400,
                "lng": 54.1880
            },
            {
                "id": 4,
                "title": "Художественная галерея",
                "type": "Галерея",
                "era": "XX век",
                "distance": "1.5 км",
                "rating": 4.7,
                "image": "🖼️",
                "lat": 52.6320,
                "lng": 54.1900
            }
        ]

    def load_events(self):
        """Загрузка событий афиши"""
        self.events = [
            {
                "id": 1,
                "name": "Выставка современного искусства",
                "date": "15 июня 2025, 18:00",
                "location": "Галерея «Новое пространство»",
                "description": "Погрузитесь в мир авангарда и инсталляций от молодых художников.",
                "age_restriction": "12+",
                "duration": "2 часа",
                "created_at": "1 июня 2025",
                "image": "https://forum.pears.fun/data/avatars/o/0/923.jpg?1718281430"
            },
            {
                "id": 2,
                "name": "Классический концерт в парке",
                "date": "20 июня 2025, 19:00",
                "location": "Центральный парк культуры",
                "description": "Симфонический оркестр исполнит лучшие произведения Чайковского и Рахманинова под открытым небом.",
                "age_restriction": "0+",
                "duration": "1.5 часа",
                "created_at": "5 июня 2025",
                "image": "🎻"
            },
            {
                "id": 3,
                "name": "Театральная премьера: «Ревизор»",
                "date": "25 июня 2025, 19:30",
                "location": "Драматический театр им. Гоголя",
                "description": "Современная интерпретация классической комедии Гоголя.",
                "age_restriction": "16+",
                "duration": "3 часа",
                "created_at": "10 июня 2025",
                "image": "🎭"
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

    def create_main_interface(self):
        """Создание основного интерфейса с поддержкой вкладок"""
        self.main_content = ft.Container(expand=True)

        self.page.add(
            ft.Column([
                self.create_header(),
                self.main_content,
                self.create_navigation()
            ], expand=True)
        )

        # Отображаем начальный экран (Карта + Рекомендации)
        self.show_main_screen()

    def create_event_card(self, event):
        """Создание карточки события с изображением и наложенным текстом"""
        # Используем Stack для наложения текста поверх изображения
        return ft.Card(
            content=ft.Container(
                content=ft.Stack(
                    controls=[
                        # Фон (заглушка под изображение)
                        ft.Container(
                            content=ft.Column([
                                ft.Image(src=event["image"], fit=ft.ImageFit.COVER, expand=True, width=float("inf"), height=float("inf") ),
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.GREY_100,
                            expand=True,
                            alignment=ft.alignment.center
                            # 🔥 Закруглённые углы:
                            
                        ),
                        # Полупрозрачный затемняющий слой
                        ft.Container(
                            bgcolor=ft.Colors.BLACK54,
                            expand=True
                        ),
                        # Текст поверх
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    event["name"],
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                ft.Text(
                                    f"📅 {event['date']}",
                                    size=12,
                                    color=ft.Colors.WHITE70
                                ),
                                ft.Text(
                                    f"📍 {event['location']}",
                                    size=12,
                                    color=ft.Colors.WHITE70
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        event["age_restriction"],
                                        size=10,
                                        color=ft.Colors.RED_200,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    bgcolor=ft.Colors.RED_800,
                                    border_radius=4,
                                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                    margin=ft.margin.only(top=4)
                                    
                                )
                            ], spacing=4),
                            padding=12,
                            alignment=ft.alignment.bottom_left,
                            expand=True
                        )
                    ]
                ),
                height=200,  # фиксированная высота для единообразия
                on_click=lambda e, ev=event: self.open_event_detail(ev)
            ),
            elevation=3,
            margin=ft.margin.symmetric(vertical=6, horizontal=4),
            shape=ft.RoundedRectangleBorder(radius=16),  # ← закруглённые углы
            clip_behavior=ft.ClipBehavior.HARD_EDGE,  # ← ОБЯЗАТЕЛЬНО!
        )

    def create_events_section(self):
        """Создание секции афиши"""
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "Афиша событий",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Column([
                    self.create_event_card(event) for event in self.events
                ], spacing=8, scroll=ft.ScrollMode.ADAPTIVE, expand=True)
            ], spacing=12, expand=True),
            padding=16,
            bgcolor=ft.Colors.WHITE,
            expand=True
        )

    def show_main_screen(self):
        """Отображение основного экрана (Карта + Рекомендации)"""
        main_content = ft.Row([
            self.create_recommendations_section()
        ], expand=True)
        self.main_content.content = main_content
        self.page.update()

    def show_events_screen(self):
        """Отображение экрана афиши"""
        self.current_view = "events"
        self.main_content.content = self.create_events_section()
        self.page.update()

    def show_catalog_screen(self):
        """Заглушка для каталога"""
        self.main_content.content = ft.Container(
            content=ft.Text("Каталог достопримечательностей", size=20),
            alignment=ft.alignment.center,
            expand=True
        )
        self.page.update()

    def show_favorites_screen(self):
        self.main_content.content = ft.Container(
            content=ft.Text("Избранное", size=20),
            alignment=ft.alignment.center,
            expand=True
        )
        self.page.update()

    def show_routes_screen(self):
        self.main_content.content = ft.Container(
            content=ft.Text("Маршруты", size=20),
            alignment=ft.alignment.center,
            expand=True
        )
        self.page.update()

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
        self.current_event = None  # ← сброс деталей события при смене вкладки
        if index == 0:  # Карта
            self.show_main_screen()
        elif index == 1:  # Каталог
            self.show_catalog_screen()
        elif index == 2:  # Афиша
            self.show_events_screen()
        elif index == 3:  # Избранное
            self.show_favorites_screen()
        elif index == 4:  # Маршруты
            self.show_routes_screen()

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

    def open_event_detail(self, event):
        """Переключиться на полноэкранный экран деталей события"""
        self.current_event = event
        self.current_view = "event_detail"
        self.show_event_detail_screen()

    def show_event_detail_screen(self):
        image_ref = ft.Ref[ft.Container]()
        initial_height = 280
        min_height = 60  # ← минимальная высота при полном скролле

        def on_scroll(e):
            scroll_offset = e.pixels
            # Чем больше скролл — тем меньше изображение
            new_height = max(min_height, initial_height - scroll_offset * 0.7)  # коэффициент 0.7 для более агрессивного сжатия
            image_ref.current.height = new_height

            # Обновляем видимость названия: при маленькой высоте — показываем поверх
            if new_height <= 80:
                title_overlay.visible = True
                title_main.visible = False
            else:
                title_overlay.visible = False
                title_main.visible = True

            self.page.update()

        # Название для "большого" режима (под изображением)
        title_main = ft.Container(
            content=ft.Text(self.current_event["name"], size=24, weight=ft.FontWeight.BOLD),
            padding=ft.padding.only(left=16, right=16, top=16),
            visible=True
        )

        # Название для "маленького" режима (поверх изображения)
        title_overlay = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    on_click=self.go_back_to_events
                ),
                ft.Text(
                    self.current_event["name"],
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    expand=True,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(width=48)  # балансировка ширины кнопки
            ]),
            padding=8,
            visible=False,
            alignment=ft.alignment.center
        )

        # Изображение с наложенным названием (для компактного режима)
        image_container = ft.Container(
            content=ft.Stack([
                ft.Image(
                    src=self.current_event["image"],
                    fit=ft.ImageFit.COVER,
                    width=float("inf"),
                    height=initial_height
                ),
                title_overlay  # ← будет появляться при сжатии
            ]),
            height=initial_height,
            ref=image_ref,
            border_radius=ft.border_radius.only(bottom_left=24, bottom_right=24) if initial_height > 100 else ft.border_radius.all(0)
        )

        info_content = ft.Column([
            title_main,  # ← видно только в раскрытом режиме
            ft.Divider(height=10),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.GREY_600),
                title=ft.Text(f"Дата: {self.current_event['date']}")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.GREY_600),
                title=ft.Text(f"Место: {self.current_event['location']}")
            ),
            ft.ListTile(
                leading=ft.Text("🔞", size=18),
                title=ft.Text(f"Возраст: {self.current_event['age_restriction']}")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.TIMER, color=ft.Colors.GREY_600),
                title=ft.Text(f"Длительность: {self.current_event['duration']}")
            ),
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("Описание", size=18, weight=ft.FontWeight.BOLD),
                        padding=ft.padding.only(left=16, top=16)
                    ),
                    ft.Container(
                        content=ft.Text(self.current_event["description"]),
                        padding=ft.padding.only(left=16, right=16)
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Text(
                            f"Добавлено: {self.current_event['created_at']}",
                            size=12,
                            color=ft.Colors.GREY_600,
                            italic=True
                        ),
                        padding=ft.padding.only(left=16, top=8)
                    )
                ], spacing=8),
                bgcolor=ft.Colors.WHITE,
                expand=True
            ),
            ft.Container(
                content=ft.FilledButton("← Назад к афише", on_click=self.go_back_to_events),
                padding=16
            )
        ], spacing=0, tight=True)

        scroll_view = ft.ListView(
            controls=[
                image_container,
                info_content
            ],
            expand=True,
            on_scroll=on_scroll
        )

        self.main_content.content = scroll_view
        self.page.update()
    
    def go_back_to_events(self, e):
        """Вернуться к списку событий (афише)"""
        self.current_event = None
        self.show_events_screen()

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
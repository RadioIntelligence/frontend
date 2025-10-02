import flet as ft
import json


class CulturalApp:
    def __init__(self):
        self.page = None
        self.map_container = None
        self.recommendations = []
        self.events = []
        self.current_view = "map"  # "map", "catalog", "events", "details", "event_detail"
        self.current_place = None
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
        
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        page.vertical_alignment = ft.MainAxisAlignment.START

        self.load_recommendations()
        self.load_events()
        self.create_main_interface()

    def load_recommendations(self):
        """Загрузка рекомендаций с URL картинок"""
        self.recommendations = [
            {
                "id": 1,
                "title": "Исторический музей",
                "type": "Музей",
                "era": "XIX век",
                "distance": "1.2 км",
                "rating": 4.8,
                "image": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=300&fit=crop",
                "description": "Крупнейший исторический музей города с богатой коллекцией артефактов от древних времен до современности.",
                "address": "ул. Центральная, 15",
                "working_hours": "10:00 - 18:00",
                "price": "300 руб.",
                "phone": "+7 (495) 123-45-67",
                "website": "www.history-museum.ru",
                "lat": 52.6338,
                "lng": 54.1928
            },
            {
                "id": 2,
                "title": "Парк культуры и отдыха",
                "type": "Парк",
                "era": "Современность",
                "distance": "0.8 км",
                "rating": 4.6,
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
                "description": "Просторный парк с ухоженными аллеями, фонтанами и разнообразными развлечениями для всей семьи.",
                "address": "пр. Парковый, 1",
                "working_hours": "круглосуточно",
                "price": "бесплатно",
                "phone": "+7 (495) 234-56-78",
                "website": "www.city-park.ru",
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
                "image": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=300&fit=crop",
                "description": "Архитектурный памятник XVIII века, сохранивший атмосферу дворянской жизни.",
                "address": "ул. Дворянская, 25",
                "working_hours": "11:00 - 19:00",
                "price": "500 руб.",
                "phone": "+7 (495) 345-67-89",
                "website": "www.old-manor.ru",
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
                "image": "https://images.unsplash.com/photo-1563089145-599997674d42?w=400&h=300&fit=crop",
                "description": "Современная галерея с коллекцией произведений российских и зарубежных художников.",
                "address": "ул. Искусств, 8",
                "working_hours": "12:00 - 20:00",
                "price": "400 руб.",
                "phone": "+7 (495) 456-78-90",
                "website": "www.art-gallery.ru",
                "lat": 52.6320,
                "lng": 54.1900
            },
            {
                "id": 5,
                "title": "Кафедральный собор",
                "type": "Архитектура",
                "era": "XIX век",
                "distance": "1.8 км",
                "rating": 4.9,
                "image": "https://images.unsplash.com/photo-1438032005730-c779502df39b?w=400&h=300&fit=crop",
                "description": "Величественный православный собор с уникальной архитектурой и богатой историей.",
                "address": "пл. Соборная, 3",
                "working_hours": "07:00 - 20:00",
                "price": "бесплатно",
                "phone": "+7 (495) 567-89-01",
                "website": "www.cathedral.ru"
            },
            {
                "id": 6,
                "title": "Театр оперы и балета",
                "type": "Театр",
                "era": "XX век",
                "distance": "1.3 км",
                "rating": 4.8,
                "image": "https://images.unsplash.com/photo-1541336032412-2048a678540d?w=400&h=300&fit=crop",
                "description": "Ведущий театр города с богатым репертуаром классических и современных постановок.",
                "address": "пр. Театральный, 12",
                "working_hours": "касса: 10:00 - 21:00",
                "price": "от 800 руб.",
                "phone": "+7 (495) 678-90-12",
                "website": "www.opera-ballet.ru"
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
                "image": "https://images.unsplash.com/photo-1563089145-599997674d42?w=400&h=300&fit=crop"
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
                "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop"
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
                "image": "https://images.unsplash.com/photo-1541336032412-2048a678540d?w=400&h=300&fit=crop"
            }
        ]

    def create_search_bar(self):
        """Создание поисковой строки для мобильных"""
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.SEARCH, color=ft.Colors.GREY_600),
                    padding=ft.padding.only(left=8)
                ),
                ft.TextField(
                    hint_text="Поиск достопримечательностей...",
                    border=ft.InputBorder.NONE,
                    expand=True,
                    text_size=14,
                    content_padding=ft.padding.symmetric(vertical=12, horizontal=0),
                    on_change=self.on_search_change
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.FILTER_LIST,
                        icon_color=ft.Colors.GREY_600,
                        on_click=self.open_filters,
                        style=ft.ButtonStyle(padding=ft.padding.all(4))
                    ),
                    padding=ft.padding.only(right=4)
                )
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            border_radius=25,
            margin=ft.margin.symmetric(vertical=8, horizontal=16),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 2)
            ),
            height=48
        )

    def create_header(self):
        """Создание заголовка для мобильных"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(
                        "Культурный гид",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    ft.IconButton(
                        icon=ft.Icons.ACCOUNT_CIRCLE,
                        icon_color=ft.Colors.WHITE,
                        on_click=self.open_profile,
                        icon_size=24
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.create_search_bar()
            ], spacing=0),
            bgcolor=ft.Colors.PRIMARY,
            padding=ft.padding.symmetric(vertical=12, horizontal=0),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 2)
            )
        )

    def create_navigation(self):
        """Создание навигации для мобильных"""
        nav_items = [
            {"icon": ft.Icons.MAP, "label": "Карта", "view": "map"},
            {"icon": ft.Icons.EXPLORE, "label": "Каталог", "view": "catalog"},
            {"icon": ft.Icons.EVENT, "label": "Афиша", "view": "events"},
            {"icon": ft.Icons.FAVORITE, "label": "Избранное", "view": "favorites"},
            {"icon": ft.Icons.ROUTE, "label": "Маршруты", "view": "routes"}
        ]

        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.IconButton(
                            icon=item["icon"],
                            icon_color=ft.Colors.PRIMARY if self.current_view == item["view"] else ft.Colors.GREY_600,
                            on_click=lambda e, view=item["view"]: self.on_nav_click(e, view),
                            icon_size=24,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=ft.padding.all(8)
                            )
                        ),
                        ft.Text(
                            item["label"],
                            size=10,
                            color=ft.Colors.PRIMARY if self.current_view == item["view"] else ft.Colors.GREY_600,
                            weight=ft.FontWeight.W_500 if self.current_view == item["view"] else ft.FontWeight.NORMAL
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                    spacing=2,
                    tight=True
                    ),
                    padding=ft.padding.symmetric(vertical=4, horizontal=2),
                    expand=True,
                    alignment=ft.alignment.center
                ) for item in nav_items
            ], 
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.symmetric(vertical=8, horizontal=4),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=16,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, -2)
            ),
            border=ft.border.only(top=ft.BorderSide(color=ft.Colors.GREY_200, width=1))
        )

    def create_image_container(self, image_url, size="small"):
        """Создание контейнера с изображением"""
        height = 120 if size == "small" else 250
        return ft.Container(
            content=ft.Image(
                src=image_url,
                fit=ft.ImageFit.COVER,
                width=float("inf"),
                height=height,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.GREY_300,
            border_radius=ft.border_radius.only(
                top_left=12, 
                top_right=12
            ) if size == "small" else 12,
            height=height,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )

    def create_place_card(self, item):
        """Создание карточки достопримечательности с полной информацией"""
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        # Изображение
                        self.create_image_container(item["image"], "small"),
                        
                        # Информация - теперь с фиксированной высотой и без обрезания текста
                        ft.Container(
                            content=ft.Column([
                                # Название - всегда полностью видно
                                ft.Container(
                                    content=ft.Text(
                                        item["title"],
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER,
                                        max_lines=2,
                                        overflow=ft.TextOverflow.VISIBLE
                                    ),
                                    padding=ft.padding.only(bottom=6)
                                ),
                                
                                # Тип и рейтинг в одной строке
                                ft.Container(
                                    content=ft.Row([
                                        ft.Container(
                                            content=ft.Text(
                                                item["type"],
                                                size=11,
                                                color=ft.Colors.BLUE_700
                                            ),
                                            bgcolor=ft.Colors.BLUE_50,
                                            border_radius=6,
                                            padding=ft.padding.symmetric(horizontal=8, vertical=4)
                                        ),
                                        ft.Text(
                                            f"⭐ {item['rating']}",
                                            size=11,
                                            color=ft.Colors.AMBER,
                                            weight=ft.FontWeight.W_500
                                        )
                                    ], 
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=8,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                    padding=ft.padding.only(bottom=6)
                                ),
                                
                                # Расстояние и эпоха
                                ft.Container(
                                    content=ft.Row([
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.Icons.LOCATION_ON, size=12, color=ft.Colors.GREY_600),
                                                ft.Text(
                                                    item["distance"],
                                                    size=11,
                                                    color=ft.Colors.GREY_700
                                                )
                                            ], spacing=4),
                                        ),
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.Icons.ACCESS_TIME, size=12, color=ft.Colors.GREY_600),
                                                ft.Text(
                                                    item["era"],
                                                    size=11,
                                                    color=ft.Colors.GREY_700
                                                )
                                            ], spacing=4),
                                        )
                                    ], 
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                    padding=ft.padding.symmetric(horizontal=4)
                                )
                            ], 
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            tight=True
                            ),
                            padding=ft.padding.all(10),
                            height=110  # Фиксированная высота для информационного блока
                        )
                    ], spacing=0),
                    on_click=lambda e, item=item: self.open_place_detail(item),
                    border_radius=12
                ),
                elevation=3,
                margin=0
            ),
            margin=ft.margin.symmetric(horizontal=4, vertical=4),
            width=175,
            height=250
        )

    def create_catalog_view(self):
        """Создание вида каталога для мобильных"""
        grid = ft.GridView(
            runs_count=2,
            max_extent=175,
            spacing=8,
            run_spacing=8,
            padding=16,
            child_aspect_ratio=0.7,
        )
        
        for item in self.recommendations:
            grid.controls.append(self.create_place_card(item))
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Каталог достопримечательностей", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text("Выберите место для просмотра подробной информации", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER)
                ], spacing=4),
                padding=ft.padding.symmetric(vertical=16, horizontal=16)
            ),
            ft.Divider(height=1),
            ft.Container(content=grid, expand=True)
        ], spacing=0)

    def create_place_detail_view(self, place):
        """Создание детального просмотра места с большим изображением"""
        return ft.Column([
            # Заголовок с кнопкой назад
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.show_catalog(),
                        icon_size=24,
                        style=ft.ButtonStyle(
                            padding=ft.padding.all(8)
                        )
                    ),
                    ft.Text(
                        place["title"],
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.FAVORITE_BORDER,
                        on_click=lambda e: self.toggle_favorite(place["id"]),
                        icon_size=24,
                        style=ft.ButtonStyle(
                            padding=ft.padding.all(8)
                        )
                    )
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.symmetric(vertical=8, horizontal=12),
                bgcolor=ft.Colors.WHITE,
                border=ft.border.only(bottom=ft.BorderSide(color=ft.Colors.GREY_200, width=1))
            ),
            
            # Контент с прокруткой
            ft.Container(
                content=self.create_place_detail_content(place),
                expand=True
            )
        ])

    def create_place_detail_content(self, place):
        """Создание содержимого детальной страницы с изображением"""
        return ft.ListView(
            controls=[
                # Большое изображение
                self.create_image_container(place["image"], "large"),
                
                # Основная информация
                ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.CATEGORY, size=20),
                            title=ft.Text("Тип", size=12, color=ft.Colors.GREY_600),
                            subtitle=ft.Text(place["type"], size=14),
                            dense=True
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.STAR, size=20),
                            title=ft.Text("Рейтинг", size=12, color=ft.Colors.GREY_600),
                            subtitle=ft.Text(f"{place['rating']} ⭐", size=14),
                            dense=True
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOCATION_ON, size=20),
                            title=ft.Text("Адрес", size=12, color=ft.Colors.GREY_600),
                            subtitle=ft.Text(place["address"], size=14),
                            dense=True
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ACCESS_TIME, size=20),
                            title=ft.Text("Время работы", size=12, color=ft.Colors.GREY_600),
                            subtitle=ft.Text(place["working_hours"], size=14),
                            dense=True
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ATTACH_MONEY, size=20),
                            title=ft.Text("Стоимость", size=12, color=ft.Colors.GREY_600),
                            subtitle=ft.Text(place["price"], size=14),
                            dense=True
                        ),
                    ], spacing=0),
                    padding=ft.padding.symmetric(vertical=8)
                ),
                
                # Описание
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Описание",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            place["description"],
                            size=14,
                            color=ft.Colors.GREY_700
                        )
                    ]),
                    padding=16,
                    bgcolor=ft.Colors.GREY_50
                ),
                
                # Контакты
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Контакты",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800
                        ),
                        ft.Container(height=12),
                        ft.Row([
                            ft.Icon(ft.Icons.PHONE, size=18, color=ft.Colors.GREY_600),
                            ft.Container(width=12),
                            ft.Text(place["phone"], size=14, expand=True)
                        ]),
                        ft.Container(height=8),
                        ft.Row([
                            ft.Icon(ft.Icons.LANGUAGE, size=18, color=ft.Colors.GREY_600),
                            ft.Container(width=12),
                            ft.Text(place["website"], size=14, expand=True)
                        ])
                    ]),
                    padding=16
                ),
                
                # Кнопки действий
                ft.Container(
                    content=ft.Row([
                        ft.FilledButton(
                            "Построить маршрут",
                            icon=ft.Icons.DIRECTIONS,
                            on_click=lambda e: self.build_route(place),
                            expand=True,
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(vertical=16)
                            )
                        ),
                    ]),
                    padding=16
                ),
                
                ft.Container(height=20)
            ],
            spacing=0,
            padding=0
        )

    def create_map_view(self):
        """Создание вида карты для мобильных"""
        return ft.Column([
            ft.Container(
                content=ft.Text(
                    "Карта достопримечательностей",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                padding=16
            ),
            ft.Container(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.MAP, size=64, color=ft.Colors.GREY_400),
                        ft.Text(
                            "Интерактивная карта",
                            size=16,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=16),
                        ft.FilledButton(
                            "Открыть карту",
                            icon=ft.Icons.OPEN_IN_FULL,
                            on_click=self.open_full_map
                        )
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER, 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.GREY_100,
                    alignment=ft.alignment.center,
                    margin=16,
                    border_radius=12,
                    height=300
                ),
                expand=True
            )
        ])

    def create_event_card(self, event):
        """Создание карточки события с изображением и наложенным текстом"""
        return ft.Card(
            content=ft.Container(
                content=ft.Stack(
                    controls=[
                        # Изображение
                        ft.Image(
                            src=event["image"],
                            fit=ft.ImageFit.COVER,
                            width=float("inf"),
                            height=200
                        ),
                        # Полупрозрачный затемняющий слой
                        ft.Container(
                            bgcolor=ft.Colors.BLACK54,
                            height=200
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
                            alignment=ft.alignment.bottom_left
                        )
                    ]
                ),
                height=200,
                on_click=lambda e, ev=event: self.open_event_detail(ev)
            ),
            elevation=3,
            margin=ft.margin.symmetric(vertical=6, horizontal=4),
            shape=ft.RoundedRectangleBorder(radius=16),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

    def create_events_view(self):
        """Создание вида афиши"""
        return ft.Column([
            ft.Container(
                content=ft.Text(
                    "Афиша событий",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                padding=16
            ),
            ft.Container(
                content=ft.Column([
                    self.create_event_card(event) for event in self.events
                ], scroll=ft.ScrollMode.ADAPTIVE),
                expand=True
            )
        ], spacing=0)

    def create_event_detail_view(self, event):
        """Создание детального просмотра события"""
        image_ref = ft.Ref[ft.Container]()
        initial_height = 280
        min_height = 60

        def on_scroll(e):
            scroll_offset = e.pixels
            new_height = max(min_height, initial_height - scroll_offset * 0.7)
            image_ref.current.height = new_height

            if new_height <= 80:
                title_overlay.visible = True
                title_main.visible = False
            else:
                title_overlay.visible = False
                title_main.visible = True

            self.page.update()

        # Название для "большого" режима
        title_main = ft.Container(
            content=ft.Text(event["name"], size=24, weight=ft.FontWeight.BOLD),
            padding=ft.padding.only(left=16, right=16, top=16),
            visible=True
        )

        # Название для "маленького" режима
        title_overlay = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    on_click=self.go_back_to_events
                ),
                ft.Text(
                    event["name"],
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    expand=True,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(width=48)
            ]),
            padding=8,
            visible=False,
            alignment=ft.alignment.center
        )

        # Изображение с наложенным названием
        image_container = ft.Container(
            content=ft.Stack([
                ft.Image(
                    src=event["image"],
                    fit=ft.ImageFit.COVER,
                    width=float("inf"),
                    height=initial_height
                ),
                title_overlay
            ]),
            height=initial_height,
            ref=image_ref
        )

        info_content = ft.Column([
            title_main,
            ft.Divider(height=10),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.GREY_600),
                title=ft.Text(f"Дата: {event['date']}")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.GREY_600),
                title=ft.Text(f"Место: {event['location']}")
            ),
            ft.ListTile(
                leading=ft.Text("🔞", size=18),
                title=ft.Text(f"Возраст: {event['age_restriction']}")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.TIMER, color=ft.Colors.GREY_600),
                title=ft.Text(f"Длительность: {event['duration']}")
            ),
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("Описание", size=18, weight=ft.FontWeight.BOLD),
                        padding=ft.padding.only(left=16, top=16)
                    ),
                    ft.Container(
                        content=ft.Text(event["description"]),
                        padding=ft.padding.only(left=16, right=16)
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Text(
                            f"Добавлено: {event['created_at']}",
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

        return ft.ListView(
            controls=[
                image_container,
                info_content
            ],
            expand=True,
            on_scroll=on_scroll
        )

    def create_main_interface(self):
        """Создание основного интерфейса для мобильных"""
        self.content_area = ft.Container(content=self.create_map_view(), expand=True)
        
        main_layout = ft.Column([
            self.create_header(),
            self.content_area,
            self.create_navigation()
        ], spacing=0, expand=True)
        
        self.page.add(main_layout)

    def switch_view(self, view_name, data=None):
        """Переключение между видами"""
        self.current_view = view_name
        
        if view_name == "map":
            self.content_area.content = self.create_map_view()
        elif view_name == "catalog":
            self.content_area.content = self.create_catalog_view()
        elif view_name == "events":
            self.content_area.content = self.create_events_view()
        elif view_name == "details" and data:
            self.current_place = data
            self.content_area.content = self.create_place_detail_view(data)
        elif view_name == "event_detail" and data:
            self.current_event = data
            self.content_area.content = self.create_event_detail_view(data)
        
        self.page.controls[0].controls[2] = self.create_navigation()
        self.page.update()

    def show_catalog(self):
        """Показать каталог"""
        self.switch_view("catalog")

    def show_map(self):
        """Показать карту"""
        self.switch_view("map")

    def show_events(self):
        """Показать афишу"""
        self.switch_view("events")

    def open_place_detail(self, place):
        """Открыть детальную информацию о месте"""
        self.switch_view("details", place)

    def open_event_detail(self, event):
        """Открыть детальную информацию о событии"""
        self.switch_view("event_detail", event)

    def go_back_to_events(self, e):
        """Вернуться к списку событий"""
        self.switch_view("events")

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

    def on_nav_click(self, e, view):
        """Обработчик клика по навигации"""
        if view in ["map", "catalog", "events"]:
            self.switch_view(view)
        else:
            print(f"Навигация: {view}")

    def toggle_favorite(self, place_id):
        """Добавить/удалить из избранного"""
        print(f"Избранное: {place_id}")

    def build_route(self, place):
        """Построить маршрут"""
        print(f"Построение маршрута к: {place['title']}")

    def open_full_map(self, e):
        """Открытие полной карты"""
        print("Открытие полной карты")


if __name__ == "__main__":
    app = CulturalApp()
    ft.app(target=app.main, view=ft.AppView.FLET_APP)
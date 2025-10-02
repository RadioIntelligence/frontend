import flet as ft
from models.models import Place
from services.map_service import MapService

class MapView:
    def __init__(self, map_service: MapService, on_place_click=None, on_full_map_click=None):
        self.map_service = map_service
        self.on_place_click = on_place_click
        self.on_full_map_click = on_full_map_click

    def create_map_container(self):
        """Создание контейнера для карты"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.MAP, size=64, color=ft.Colors.GREY_400),
                ft.Text(
                    "Карта достопримечательностей",
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=16),
                ft.FilledButton(
                    "Открыть карту",
                    icon=ft.Icons.OPEN_IN_FULL,
                    on_click=self.on_full_map_click
                )
            ], 
            alignment=ft.MainAxisAlignment.CENTER, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.GREY_100,
            alignment=ft.alignment.center,
            margin=16,
            border_radius=12,
            height=300
        )

    def create_full_map_view(self, places: list[Place]):
        """Создание полноэкранной карты с маркерами"""
        # Инициализация карты
        map_api = self.map_service.initialize_map(
            "full-map-container", 
            {"center": [52.970756, 36.064358], "zoom": 12}
        )
        
        # Добавление маркеров для всех мест
        for place in places:
            if place.lat and place.lng:
                map_api['add_marker'](place.lat, place.lng, place.title)

        # Пример добавления стандартных маркеров
        map_api['add_marker'](52.962197, 36.064894, "Памятник Н. С. Лескову")
        map_api['add_marker'](52.961665, 36.065917, "Памятник А. П. Ермолову")
        map_api['add_marker'](52.967952, 36.064322, "Академический театр им. И.С. Тургенева")
        map_api['set_center'](52.970756, 36.064358)

        return ft.Column([
            # Заголовок с кнопкой назад
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.on_full_map_click() if self.on_full_map_click else None,
                        icon_size=24
                    ),
                    ft.Text(
                        "Интерактивная карта",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(width=48)  # для балансировки
                ]),
                padding=ft.padding.symmetric(vertical=8, horizontal=12),
                bgcolor=ft.Colors.WHITE,
                border=ft.border.only(bottom=ft.BorderSide(color=ft.Colors.GREY_200, width=1))
            ),
            
            # Контейнер карты
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.MAP, size=80, color=ft.Colors.PRIMARY),
                    ft.Text(
                        "Карта достопримечательностей",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "В реальном приложении здесь будет интерактивная карта\nс маркерами достопримечательностей",
                        size=14,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "Добавленные маркеры:",
                        size=16,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(height=10),
                    *[
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.RED),
                            title=ft.Text(marker['title']),
                            subtitle=ft.Text(f"Широта: {marker['lat']:.4f}, Долгота: {marker['lng']:.4f}")
                        ) for marker in self.map_service.get_map_data("full-map-container").get('markers', [])[:5]
                    ]
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.GREY_50,
                alignment=ft.alignment.center,
                margin=16,
                border_radius=12,
                padding=20,
                expand=True
            )
        ])

    def create_view(self, places: list[Place], full_screen: bool = False):
        """Создание вида карты"""
        if full_screen:
            return self.create_full_map_view(places)
        else:
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
                    content=self.create_map_container(),
                    expand=True
                )
            ])
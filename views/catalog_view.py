import flet as ft
from models.models import Place

class CatalogView:
    def __init__(self, on_place_click=None):
        self.on_place_click = on_place_click

    def create_image_container(self, image_url: str, size: str = "small"):
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

    def create_place_card(self, place: Place):
        """Создание карточки достопримечательности"""
        return ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        # Изображение
                        self.create_image_container(place.image, "small"),
                        
                        # Информация
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Text(
                                        place.title,
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER,
                                        max_lines=2,
                                        overflow=ft.TextOverflow.VISIBLE
                                    ),
                                    padding=ft.padding.only(bottom=6)
                                ),
                                
                                ft.Container(
                                    content=ft.Row([
                                        ft.Container(
                                            content=ft.Text(
                                                place.type,
                                                size=11,
                                                color=ft.Colors.BLUE_700
                                            ),
                                            bgcolor=ft.Colors.BLUE_50,
                                            border_radius=6,
                                            padding=ft.padding.symmetric(horizontal=8, vertical=4)
                                        ),
                                        ft.Text(
                                            f"⭐ {place.rating}",
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
                                
                                ft.Container(
                                    content=ft.Row([
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.Icons.LOCATION_ON, size=12, color=ft.Colors.GREY_600),
                                                ft.Text(
                                                    place.distance,
                                                    size=11,
                                                    color=ft.Colors.GREY_700
                                                )
                                            ], spacing=4),
                                        ),
                                        ft.Container(
                                            content=ft.Row([
                                                ft.Icon(ft.Icons.ACCESS_TIME, size=12, color=ft.Colors.GREY_600),
                                                ft.Text(
                                                    place.era,
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
                            height=110
                        )
                    ], spacing=0),
                    on_click=lambda e, place=place: self.on_place_click(place) if self.on_place_click else None,
                    border_radius=12
                ),
                elevation=3,
                margin=0
            ),
            margin=ft.margin.symmetric(horizontal=4, vertical=4),
            width=175,
            height=250
        )

    def create_view(self, places: list[Place]):
        """Создание вида каталога"""
        grid = ft.GridView(
            runs_count=2,
            max_extent=175,
            spacing=8,
            run_spacing=8,
            padding=16,
            child_aspect_ratio=0.7,
        )
        
        for place in places:
            grid.controls.append(self.create_place_card(place))
        
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
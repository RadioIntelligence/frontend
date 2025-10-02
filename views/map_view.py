import flet as ft
from models.models import Place

class MapView:
    def __init__(self, on_place_click=None, on_full_map_click=None):
        self.on_place_click = on_place_click
        self.on_full_map_click = on_full_map_click

    def create_view(self, places: list[Place]):
        """Создание вида карты"""
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
                ),
                expand=True
            )
        ])
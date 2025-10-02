import flet as ft

class RoutesView:
    def create_view(self):
        """Создание вида маршрутов"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Маршруты", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Здесь будут ваши маршруты", size=16, color=ft.Colors.GREY_600)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )
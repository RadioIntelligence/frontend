import flet as ft

class FavoritesView:
    def create_view(self):
        """Создание вида избранного"""
        return ft.Container(
            content=ft.Column([
                ft.Text("Избранное", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Здесь будут ваши избранные места", size=16, color=ft.Colors.GREY_600)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True
        )
import flet as ft
import asyncio
from models.data_loader import load_places, load_events
from views.map_view import MapView
from views.catalog_view import CatalogView
from views.events_view import EventsView
from views.favorites_view import FavoritesView
from views.routes_view import RoutesView
from views.auth_view import AuthView
from views.profile_view import ProfileView
from services.auth_service import AuthService
from services.map_service import MapService
from services.event_service import EventsService
from models.models import Place, Event

class CulturalApp:
    def __init__(self):
        self.page = None
        self.places = []
        self.events = []
        self.current_view = "auth"
        self.current_place = None
        self.current_event = None
        self.full_screen_map = False
        self._auto_update_task = None
        
        # Инициализация сервисов
        self.auth_service = AuthService()
        self.map_service = MapService()
        self.events_service = EventsService(auth_service=self.auth_service)
        
        # Инициализация вьюшек
        self.auth_view = AuthView(
            auth_service=self.auth_service,
            on_login_success=self.on_login_success,  # Теперь это асинхронный метод
            on_show_register=self.show_register_screen,
            on_show_login=self.show_login_screen
        )
        self.profile_view = ProfileView(
            auth_service=self.auth_service,
            on_logout=self.logout,
            on_back=self.go_back_to_main
        )
        self.map_view = MapView(
            map_service=self.map_service,
            on_place_click=self.open_place_detail,
            on_full_map_click=self.toggle_full_map
        )
        self.catalog_view = CatalogView(on_place_click=self.open_place_detail)
        self.events_view = EventsView(
            on_event_click=self.open_event_detail,
            on_back_click=self.go_back_to_events
        )
        self.favorites_view = FavoritesView()
        self.routes_view = RoutesView()

    async def main(self, page: ft.Page):
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

        # Устанавливаем страницу в auth_view
        self.auth_view.set_page(page)

        # Проверка аутентификации
        if self.auth_service.is_authenticated():
            await self.load_data()
            self.create_main_interface()
            self.switch_view("map")
            
            # Запуск автоматического обновления событий
            self._auto_update_task = asyncio.create_task(self.start_events_auto_update())
        else:
            self.show_login_screen()

    def show_login_screen(self):
        """Показать экран входа"""
        self.current_view = "auth"
        self.page.clean()
        login_view = self.auth_view.create_login_view()
        self.page.add(login_view)
        self.page.update()

    def show_register_screen(self):
        """Показать экран регистрации"""
        self.current_view = "auth"
        self.page.clean()
        register_view = self.auth_view.create_register_view()
        self.page.add(register_view)
        self.page.update()

    async def on_login_success(self):
        """Обработчик успешного входа (теперь асинхронный)"""
        await self.load_data()
        self.create_main_interface()
        self.switch_view("map")
        
        # Запуск автоматического обновления после входа
        if self._auto_update_task:
            self._auto_update_task.cancel()
        self._auto_update_task = asyncio.create_task(self.start_events_auto_update())

    async def load_data(self):
        """Асинхронная загрузка данных"""
        # Загружаем места из локальных данных
        self.places = load_places()
        
        try:
            # Пытаемся загрузить события с API
            self.events = await self.events_service.fetch_events_from_api()
            if not self.events:
                # Fallback на мок-данные
                self.events = load_events()
                print("Используются локальные данные событий")
            else:
                print(f"Загружено {len(self.events)} событий с API")
        except Exception as e:
            print(f"Ошибка загрузки событий с API: {e}")
            self.events = load_events()
            print("Используются локальные данные событий")

    async def start_events_auto_update(self):
        """Запуск автоматического обновления событий"""
        try:
            await self.events_service.start_auto_update(self.update_events_callback)
        except asyncio.CancelledError:
            print("Автообновление событий остановлено")
        except Exception as e:
            print(f"Ошибка в автообновлении событий: {e}")

    def update_events_callback(self, new_events: list):
        """Колбэк для обновления событий в UI"""
        if new_events:
            self.events = new_events
            
            # Обновляем UI если текущий вид - события
            if self.current_view == "events":
                self.switch_view("events")
            
            # Показываем уведомление о обновлении
            self.show_update_notification(f"Обновлено {len(new_events)} событий")

    def show_update_notification(self, message: str):
        """Показать уведомление об обновлении"""
        if hasattr(self, 'page') and self.page:
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(message),
                    action="OK",
                    duration=3000
                )
            )

    def create_search_bar(self):
        """Создание поисковой строки"""
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
        """Создание заголовка"""
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
        """Создание навигации"""
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

    def create_main_interface(self):
        """Создание основного интерфейса"""
        self.content_area = ft.Container(expand=True)
        
        main_layout = ft.Column([
            self.create_header(),
            self.content_area,
            self.create_navigation()
        ], spacing=0, expand=True)
        
        self.page.clean()
        self.page.add(main_layout)
        self.page.update()

    def switch_view(self, view_name: str, data=None):
        """Переключение между видами"""
        self.current_view = view_name
        
        if view_name == "map":
            if self.full_screen_map:
                self.content_area.content = self.map_view.create_view(self.places, full_screen=True)
            else:
                self.content_area.content = self.map_view.create_view(self.places)
        elif view_name == "catalog":
            self.content_area.content = self.catalog_view.create_view(self.places)
        elif view_name == "events":
            self.content_area.content = self.events_view.create_view(self.events)
        elif view_name == "favorites":
            self.content_area.content = self.favorites_view.create_view()
        elif view_name == "routes":
            self.content_area.content = self.routes_view.create_view()
        elif view_name == "profile":
            self.content_area.content = self.profile_view.create_profile_view()
        elif view_name == "place_detail" and data:
            self.current_place = data
            self.content_area.content = self.create_place_detail_view(data)
        elif view_name == "event_detail" and data:
            self.current_event = data
            self.content_area.content = self.events_view.create_view(
                self.events, show_detail=True, selected_event=data
            )
        
        # Обновляем навигацию
        if self.page.controls and len(self.page.controls[0].controls) > 2:
            self.page.controls[0].controls[2] = self.create_navigation()
        self.page.update()

    def create_place_detail_view(self, place: Place):
        """Создание детального просмотра места"""
        return ft.Column([
            # Заголовок с кнопкой назад
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: self.switch_view("catalog"),
                        icon_size=24,
                        style=ft.ButtonStyle(padding=ft.padding.all(8))
                    ),
                    ft.Text(place.title, size=18, weight=ft.FontWeight.BOLD, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.FAVORITE_BORDER,
                        on_click=lambda e: self.toggle_favorite(place.id),
                        icon_size=24,
                        style=ft.ButtonStyle(padding=ft.padding.all(8))
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

    def create_place_detail_content(self, place: Place):
        """Создание содержимого детальной страницы"""
        return ft.ListView(
            controls=[
                # Изображение
                ft.Container(
                    content=ft.Image(
                        src=place.image,
                        fit=ft.ImageFit.COVER,
                        width=float("inf"),
                        height=250,
                    ),
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.GREY_300,
                    border_radius=12,
                    height=250,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE
                ),
                
                # Основная информация
                ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.CATEGORY, size=20),
                            title=ft.Text("Тип", size=12, color=ft.Colors.GREY_600),
                            subtitle=ft.Text(place.type, size=14)
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.STAR, size=20),
                            title=ft.Text("Рейтинг", size=12, color=ft.Colors.GREY_600),
                            subtitle=ft.Text(f"{place.rating} ⭐", size=14)
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOCATION_ON, size=20),
                            title=ft.Text("Адрес", size=12, color=ft.Colors.GREY_600),
                            subtitle=ft.Text(place.address, size=14)
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ACCESS_TIME, size=20),
                            title=ft.Text("Время работы", size=12, color=ft.Colors.GREY_600),
                            subtitle=ft.Text(place.working_hours, size=14)
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ATTACH_MONEY, size=20),
                            title=ft.Text("Стоимость", size=12, color=ft.Colors.GREY_600),
                            subtitle=ft.Text(place.price, size=14)
                        ),
                    ], spacing=0),
                    padding=ft.padding.symmetric(vertical=8)
                ),
                
                # Описание
                ft.Container(
                    content=ft.Column([
                        ft.Text("Описание", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Container(height=8),
                        ft.Text(place.description, size=14, color=ft.Colors.GREY_700)
                    ]),
                    padding=16,
                    bgcolor=ft.Colors.GREY_50
                ),
                
                # Контакты
                ft.Container(
                    content=ft.Column([
                        ft.Text("Контакты", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Container(height=12),
                        ft.Row([
                            ft.Icon(ft.Icons.PHONE, size=18, color=ft.Colors.GREY_600),
                            ft.Container(width=12),
                            ft.Text(place.phone, size=14, expand=True)
                        ]),
                        ft.Container(height=8),
                        ft.Row([
                            ft.Icon(ft.Icons.LANGUAGE, size=18, color=ft.Colors.GREY_600),
                            ft.Container(width=12),
                            ft.Text(place.website, size=14, expand=True)
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
                            style=ft.ButtonStyle(padding=ft.padding.symmetric(vertical=16))
                        ),
                    ]),
                    padding=16
                ),
                
                ft.Container(height=20)
            ],
            spacing=0,
            padding=0
        )

    def open_profile(self, e):
        """Открытие страницы профиля"""
        self.switch_view("profile")

    def go_back_to_main(self, e=None):
        """Возврат к главному экрану"""
        self.switch_view("map")

    def logout(self, e=None):
        """Выход из системы"""
        # Останавливаем автообновление
        if self._auto_update_task:
            self._auto_update_task.cancel()
            
        self.auth_service.logout()
        self.show_login_screen()

    def toggle_full_map(self, e=None):
        """Переключение режима полноэкранной карты"""
        self.full_screen_map = not self.full_screen_map
        self.switch_view("map")

    def on_nav_click(self, e, view):
        """Обработчик клика по навигации"""
        self.full_screen_map = False
        self.switch_view(view)

    def open_place_detail(self, place: Place):
        self.switch_view("place_detail", place)

    def open_event_detail(self, event: Event):
        self.switch_view("event_detail", event)

    def go_back_to_events(self, e):
        self.switch_view("events")

    def on_search_change(self, e):
        print(f"Поиск: {e.control.value}")

    def open_filters(self, e):
        print("Открытие фильтров")

    def toggle_favorite(self, place_id):
        print(f"Избранное: {place_id}")

    def build_route(self, place):
        print(f"Построение маршрута к: {place.title}")

    def cleanup(self):
        """Очистка ресурсов при закрытии приложения"""
        if self._auto_update_task:
            self._auto_update_task.cancel()

if __name__ == "__main__":
    app = CulturalApp()
    try:
        ft.app(target=app.main, view=ft.AppView.FLET_APP)
    finally:
        app.cleanup()
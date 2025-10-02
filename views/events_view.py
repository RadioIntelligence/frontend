import flet as ft
from models.models import Event

class EventsView:
    def __init__(self, on_event_click=None, on_back_click=None):
        self.on_event_click = on_event_click
        self.on_back_click = on_back_click

    def create_event_card(self, event: Event):
        """Создание карточки события"""
        return ft.Card(
            content=ft.Container(
                content=ft.Stack(
                    controls=[
                        ft.Image(
                            src=event.image,
                            fit=ft.ImageFit.COVER,
                            width=float("inf"),
                            height=200
                        ),
                        ft.Container(
                            bgcolor=ft.Colors.BLACK54,
                            height=200
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    event.name,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                ft.Text(
                                    f"📅 {event.date}",
                                    size=12,
                                    color=ft.Colors.WHITE70
                                ),
                                ft.Text(
                                    f"📍 {event.location}",
                                    size=12,
                                    color=ft.Colors.WHITE70
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        event.age_restriction,
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
                on_click=lambda e, event=event: self.on_event_click(event) if self.on_event_click else None
            ),
            elevation=3,
            margin=ft.margin.symmetric(vertical=6, horizontal=4),
            shape=ft.RoundedRectangleBorder(radius=16),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

    def create_events_list_view(self, events: list[Event]):
        """Создание списка событий"""
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
                    self.create_event_card(event) for event in events
                ], scroll=ft.ScrollMode.ADAPTIVE),
                expand=True
            )
        ], spacing=0)

    def create_event_detail_view(self, event: Event):
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

            # Нужно получить доступ к page через контекст
            import flet as ft
            ft.Page.update()

        title_main = ft.Container(
            content=ft.Text(event.name, size=24, weight=ft.FontWeight.BOLD),
            padding=ft.padding.only(left=16, right=16, top=16),
            visible=True
        )

        title_overlay = ft.Container(
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    on_click=self.on_back_click
                ),
                ft.Text(
                    event.name,
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

        image_container = ft.Container(
            content=ft.Stack([
                ft.Image(
                    src=event.image,
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
                title=ft.Text(f"Дата: {event.date}")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.GREY_600),
                title=ft.Text(f"Место: {event.location}")
            ),
            ft.ListTile(
                leading=ft.Text("🔞", size=18),
                title=ft.Text(f"Возраст: {event.age_restriction}")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.TIMER, color=ft.Colors.GREY_600),
                title=ft.Text(f"Длительность: {event.duration}")
            ),
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("Описание", size=18, weight=ft.FontWeight.BOLD),
                        padding=ft.padding.only(left=16, top=16)
                    ),
                    ft.Container(
                        content=ft.Text(event.description),
                        padding=ft.padding.only(left=16, right=16)
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Text(
                            f"Добавлено: {event.created_at}",
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
                content=ft.FilledButton("← Назад к афише", on_click=self.on_back_click),
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

    def create_view(self, events: list[Event], show_detail: bool = False, selected_event: Event = None):
        """Создание вида афиши"""
        if show_detail and selected_event:
            return self.create_event_detail_view(selected_event)
        else:
            return self.create_events_list_view(events)
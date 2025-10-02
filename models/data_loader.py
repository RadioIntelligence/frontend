from .models import Place, Event

def load_places():
    """Загрузка данных о достопримечательностях"""
    return [
        Place(
            id=1,
            title="Исторический музей",
            type="Музей",
            era="XIX век",
            distance="1.2 км",
            rating=4.8,
            image="https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=300&fit=crop",
            description="Крупнейший исторический музей города с богатой коллекцией артефактов от древних времен до современности.",
            address="ул. Центральная, 15",
            working_hours="10:00 - 18:00",
            price="300 руб.",
            phone="+7 (495) 123-45-67",
            website="www.history-museum.ru",
            lat=52.6338,
            lng=54.1928
        ),
        Place(
            id=2,
            title="Парк культуры и отдыха",
            type="Парк",
            era="Современность",
            distance="0.8 км",
            rating=4.6,
            image="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
            description="Просторный парк с ухоженными аллеями, фонтанами и разнообразными развлечениями для всей семьи.",
            address="пр. Парковый, 1",
            working_hours="круглосуточно",
            price="бесплатно",
            phone="+7 (495) 234-56-78",
            website="www.city-park.ru",
            lat=52.6300,
            lng=54.1950
        ),
        # ... остальные места
    ]

def load_events():
    """Загрузка данных о событиях"""
    return [
        Event(
            id=1,
            name="Выставка современного искусства",
            date="15 июня 2025, 18:00",
            location="Галерея «Новое пространство»",
            description="Погрузитесь в мир авангарда и инсталляций от молодых художников.",
            age_restriction="12+",
            duration="2 часа",
            created_at="1 июня 2025",
            image="https://images.unsplash.com/photo-1563089145-599997674d42?w=400&h=300&fit=crop"
        ),
        Event(
            id=2,
            name="Классический концерт в парке",
            date="20 июня 2025, 19:00",
            location="Центральный парк культуры",
            description="Симфонический оркестр исполнит лучшие произведения Чайковского и Рахманинова под открытым небом.",
            age_restriction="0+",
            duration="1.5 часа",
            created_at="5 июня 2025",
            image="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop"
        ),
        # ... остальные события
    ]
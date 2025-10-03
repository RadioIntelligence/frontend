import aiohttp
import asyncio
from typing import List, Optional
from datetime import datetime, timedelta
from models.models import Event

class EventsService:
    def __init__(self, api_base_url: str = "http://77.221.151.22", auth_service=None):
        self.api_base_url = api_base_url
        self.auth_service = auth_service
        self._update_interval = 300  # 5 минут
        self._is_updating = False
        self._last_update = None
        self._auto_update_running = False
        
    async def fetch_events_from_api(self) -> List[Event]:
        """Загрузка событий с API"""
        try:
            headers = self.auth_service.get_auth_headers() if self.auth_service else {}
            
            async with aiohttp.ClientSession() as session:
                # Получаем предстоящие события
                async with session.get(
                    f"{self.api_base_url}/events/",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(response.text)
                        events = await self._convert_api_events(data)
                        print(f"Успешно загружено {len(events)} событий с API")
                        return events
                    else:
                        print(f"Ошибка загрузки событий: {response.status}")
                        return []
                        
        except asyncio.TimeoutError:
            print("Таймаут при загрузке событий с API")
            return []
        except aiohttp.ClientError as e:
            print(f"Ошибка сети при загрузке событий: {e}")
            return []
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке событий: {e}")
            return []
    
    async def _convert_api_events(self, api_events: list) -> List[Event]:
        """Конвертация событий из API в клиентскую модель"""
        converted_events = []
        
        for api_event in api_events:
            try:
                # Конвертируем дату из формата API
                event_date = self._format_event_date(api_event.get('date'))
                
                event = Event(
                    id=len(converted_events) + 1,  # Временный ID
                    api_id=api_event.get('id'),
                    name=api_event.get('name', 'Событие'),
                    date=event_date,
                    location=api_event.get('location', 'Местоположение не указано'),
                    description=api_event.get('description', 'Описание отсутствует'),
                    age_restriction=f"{api_event.get('age_restriction', 0)}+",
                    duration=f"{api_event.get('duration', 60)} минут",
                    created_at=self._format_created_at(api_event.get('created_at')),
                    image=self._get_event_image(api_event.get('name')),
                    last_updated=datetime.now()
                )
                converted_events.append(event)
            except Exception as e:
                print(f"Ошибка конвертации события: {e}")
                continue
                
        return converted_events
    
    def _format_event_date(self, date_string: str) -> str:
        """Форматирование даты события"""
        try:
            if not date_string:
                return "Дата не указана"
                
            # Парсим дату из API формата
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            # Форматируем на русском
            months = {
                1: "января", 2: "февраля", 3: "марта", 4: "апреля",
                5: "мая", 6: "июня", 7: "июля", 8: "августа",
                9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
            }
            return f"{dt.day} {months[dt.month]} {dt.year}, {dt.hour:02d}:{dt.minute:02d}"
        except:
            return "Дата не указана"
    
    def _format_created_at(self, created_at: str) -> str:
        """Форматирование даты создания"""
        try:
            if not created_at:
                return datetime.now().strftime("%d %B %Y")
                
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            months = {
                1: "января", 2: "февраля", 3: "марта", 4: "апреля",
                5: "мая", 6: "июня", 7: "июля", 8: "августа",
                9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
            }
            return f"{dt.day} {months[dt.month]} {dt.year}"
        except:
            return datetime.now().strftime("%d %B %Y")
    
    def _get_event_image(self, event_name: str) -> str:
        """Получение изображения для события"""
        if not event_name:
            return "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=400&h=300&fit=crop"
        if event_name == "Цирк с симфоническим оркестром":
            return 'https://xn--e1aaodlcdmgu5b.xn--p1ai/assets/uploads/posters/2660.jpg'
        if event_name == 'Цирк "Водное шоу"':
            return 'https://1afisha.ru/image/cache/catalog/product/orel/cloud/_______________________oktyabr___________________/tsirk_vodnoe_shou_holodnoe_serdtse_-_chast_3_anna_i_elza/685922e9c04f146fa4d1d50c_1-620x400.jpg'
        if event_name == 'Дом ада. Спуск к дьяволу':
            return 'https://avatars.mds.yandex.net/get-kinopoisk-image/10703859/2919a915-5c7d-4832-8bb3-ad15036dd216/600x900'
        if event_name == 'Дракула':
            return 'https://upload.wikimedia.org/wikipedia/ru/thumb/f/f5/%D0%94%D1%80%D0%B0%D0%BA%D1%83%D0%BB%D0%B0_%28%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%2C_2025%29.jpg/500px-%D0%94%D1%80%D0%B0%D0%BA%D1%83%D0%BB%D0%B0_%28%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%2C_2025%29.jpg?20250817220859'
        
        event_name_lower = event_name.lower()
        
        

        image_mapping = {
            'концерт': 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=400&h=300&fit=crop',
            'выставка': 'https://images.unsplash.com/photo-1563089145-599997674d42?w=400&h=300&fit=crop',
            'фестиваль': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=400&h=300&fit=crop',
            'спектакль': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400&h=300&fit=crop',
            'джаз': 'https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=400&h=300&fit=crop',
            'мастер-класс': 'https://images.unsplash.com/photo-1572021335469-31706a17aaef?w=400&h=300&fit=crop',
            'экскурсия': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=400&h=300&fit=crop',
            'чтения': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop',
            'фотография': 'https://images.unsplash.com/photo-1542038784456-1ea8e935640e?w=400&h=300&fit=crop',
            'еда': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=400&h=300&fit=crop'
        }
        
        for keyword, image_url in image_mapping.items():
            if keyword in event_name_lower:
                return image_url
        
        # Дефолтное изображение
        return "https://infoorel.ru/user_foto/afisha/03d317ded260bb22b3a64c5b79e0d6a3.jpeg"
    
    def should_update_events(self) -> bool:
        """Проверка необходимости обновления событий"""
        if not self._last_update:
            return True
        
        time_since_update = datetime.now() - self._last_update
        return time_since_update.total_seconds() >= self._update_interval
    
    async def start_auto_update(self, update_callback):
        """Запуск автоматического обновления событий"""
        self._auto_update_running = True
        
        while self._auto_update_running:
            try:
                if self.should_update_events():
                    print("Автоматическое обновление событий...")
                    new_events = await self.fetch_events_from_api()
                    if new_events:
                        update_callback(new_events)
                        self._last_update = datetime.now()
                        print(f"Обновлено {len(new_events)} событий")
                    else:
                        print("Нет новых событий для обновления")
                
                # Ждем перед следующей проверкой
                await asyncio.sleep(60)  # Проверка каждую минуту
                
            except asyncio.CancelledError:
                print("Автообновление событий остановлено")
                break
            except Exception as e:
                print(f"Ошибка в автообновлении: {e}")
                await asyncio.sleep(300)  # Ждем 5 минут при ошибке
    
    def stop_auto_update(self):
        """Остановка автоматического обновления"""
        self._auto_update_running = False
        print("Автообновление событий остановлено")
class MapService:
    def __init__(self):
        self.map_instances = {}

    def initialize_map(self, container_id: str, options: dict = None) -> dict:
        """
        Инициализация карты
        В реальном приложении здесь будет интеграция с Leaflet/Google Maps
        """
        print(f'Initializing map in: {container_id}')
        
        map_instance = {
            'container_id': container_id,
            'options': options or {},
            'markers': []
        }
        
        self.map_instances[container_id] = map_instance
        
        return {
            'add_marker': lambda lat, lng, title: self.add_marker(container_id, lat, lng, title),
            'set_center': lambda lat, lng: self.set_center(container_id, lat, lng),
            'clear_markers': lambda: self.clear_markers(container_id)
        }

    def add_marker(self, container_id: str, lat: float, lng: float, title: str):
        """Добавление маркера на карту"""
        print(f'Adding marker: {lat}, {lng}, {title}')
        if container_id in self.map_instances:
            self.map_instances[container_id]['markers'].append({
                'lat': lat, 'lng': lng, 'title': title
            })

    def set_center(self, container_id: str, lat: float, lng: float):
        """Установка центра карты"""
        print(f'Setting center: {lat}, {lng}')
        if container_id in self.map_instances:
            self.map_instances[container_id]['center'] = (lat, lng)

    def clear_markers(self, container_id: str):
        """Очистка маркеров"""
        if container_id in self.map_instances:
            self.map_instances[container_id]['markers'] = []

    def get_map_data(self, container_id: str) -> dict:
        """Получение данных карты"""
        return self.map_instances.get(container_id, {})
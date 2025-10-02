import requests
from typing import Optional, Tuple

class AuthService:
    def __init__(self, api_base_url: str = "http://77.221.151.22"):
        self.api_base_url = api_base_url
        self.access_token: Optional[str] = None

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Аутентификация пользователя
        Возвращает (успех, сообщение)
        """
        try:
            response = requests.post(
                f"{self.api_base_url}/login",
                json={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                self.access_token = data["session_id"]
                return True, "Успешный вход"
            else:
                print(response.text)
                return False, "Неверный логин или пароль"
        except requests.exceptions.RequestException:
            return False, "Ошибка подключения к серверу"

    def register(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Регистрация нового пользователя
        Возвращает (успех, сообщение)
        """
        try:
            response = requests.post(
                f"{self.api_base_url}/register",
                json={"username": username, "email": email, "password": password}
            )
            if response.status_code == 200:
                return True, "Успешная регистрация"
            else:
                return False, "Ошибка регистрации"
        except requests.exceptions.RequestException:
            return False, "Ошибка подключения к серверу"

    def logout(self) -> bool:
        """Выход из системы"""
        try:
            response = requests.post(f"{self.api_base_url}/logout", headers={'Authorization':f'Bearer {self.access_token}'})
            if response.status_code == 200:
                self.access_token = None
                print("Успешный выход из системы")
                return True
            else:
                print(f"Ошибка выхода: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения при выходе: {e}")
            # Даже если сервер недоступен, очищаем токен локально
            self.access_token = None
            return True  # Возвращаем True, так как локальный выход выполнен

    def is_authenticated(self) -> bool:
        """Проверка аутентификации"""
        return self.access_token is not None

    def get_auth_headers(self) -> dict:
        """Получение заголовков для авторизованных запросов"""
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}
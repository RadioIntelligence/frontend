from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Place:
    id: int
    title: str
    type: str
    era: str
    distance: str
    rating: float
    image: str
    description: str
    address: str
    working_hours: str
    price: str
    phone: str
    website: str
    lat: Optional[float] = None
    lng: Optional[float] = None

@dataclass
class Event:
    id: int
    name: str
    date: str
    location: str
    description: str
    age_restriction: str
    duration: str
    created_at: str
    image: str

@dataclass
class UserProfile:
    name: str = "Пользователь"
    email: str = "user@example.com"
    phone: str = "+7 (XXX) XXX-XX-XX"
    bio: str = "Люблю путешествовать и открывать новые места!"
    registration_date: str = "2024"
    favorites_count: int = 5
    visited_count: int = 12
    reviews_count: int = 3
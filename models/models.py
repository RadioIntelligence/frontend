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
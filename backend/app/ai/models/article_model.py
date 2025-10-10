from dataclasses import dataclass

@dataclass
class Article:
    title: str
    subtitle: str
    date: str
    author: str
    url: str
    body: str
from dataclasses import dataclass


@dataclass
class Article:
    title: str
    author: str
    url: str
    content: str

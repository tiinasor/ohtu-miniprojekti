class Citation:
    def __init__(self, id, name: str, author: str, title: str, journal: str, year: int, volume: float, number: int, pages: str):
        self.id = id
        self.name = name
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.volume = volume
        self.number = number
        self.pages = pages      

    def __str__(self):
        return f"{self.name}: {self.title} by {self.author} ({self.year}) {self.journal}, Vol. {self.volume}, No. {self.number}, pp. {self.pages}"

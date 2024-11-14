class BookException(Exception):
    def __init__(self, isbn: str):
        self.isbn = isbn 
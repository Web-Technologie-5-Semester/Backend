class NotFoundException(Exception):
    def __init__(self, id: str, type: str):
        self.id = id 
        self.type = type


    def to_string(self) -> str:
        return f"'{self.type}' with id '{self.id}' not found"
    

class ForbiddenException(Exception):

    def to_string(self) -> str:
        return "Permission denied"
    

class ExistingException(Exception):

    def to_string(self) -> str:
        return f"'{self.type}' with id '{self.id}' already exists"
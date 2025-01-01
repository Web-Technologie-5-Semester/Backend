from sqlmodel import Session
from db import engine, get_session
from faker import Faker
import random
from inventory.models import Author, Book, Genre, Publisher
from inventory.repositories import AuthorRepository, BooksRepository, GenreRepository, PublisherRepository

fake = Faker()

def generate_books():
    session = Session(engine)
    author_ids = []
    genre_ids = []
    publisher_ids = []
    for _ in range(50):
        author = Author(name= fake.name(), birthday=fake.date());
        author_ids.append(AuthorRepository(session).create(author).id);
    

    for _ in range(50):
        publisher = Publisher(name= fake.name(), birthday=fake.date());
        publisher_ids.append(PublisherRepository(session).create(publisher).id);
    

    for _ in range(20):
        genre = Genre(name= fake.name(), birthday=fake.date());
        genre_ids.append(GenreRepository(session).create(genre).id);
    

    for _ in range(2000):
        book = Book(
            isbn= fake.isbn10(),
            title= fake.sentence(nb_words=4),
            author_id= random.choice(author_ids),
            release= fake.date(),
            genre_id= random.choice(genre_ids),
            description= fake.sentence(nb_words=200),
            price= random.randint(5, 100),
            age_recommendation= random.randint(0, 18),
            publisher_id= random.choice(publisher_ids),
            stock= random.randint(100, 300),
            image= fake.image(size=(200, 200), image_format='jpeg')
        )

        BooksRepository(session).mapping_book(book)
    
generate_books()
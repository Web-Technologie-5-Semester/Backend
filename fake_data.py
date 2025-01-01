from db import engine
from faker import Faker
import random
from inventory.models import Book

fake = Faker()

cursor = engine.connect()

def generate_books(n):
    for _ in range(n):
        book = Book(
            isbn= fake.isbn(),
            title= fake.sentence(nb_words=4),
            author= random.randint(6, 7, 9, 10),
            release= fake.date(),
            genre_id= random.randint(1, 2, 3, 4),
            description= fake.sentence(nb_words=8),
            price= fake.pricetag(),
            age_recommendation= random.randint(0, 6, 12),
            publisher= random.randint(1, 2, 3, 4),
            stock= random.randint(100, 200, 300)
        )
        cursor.execute('INSERT INTO books (isbn, title, author, release, genre, description, price, age_recommendation, publisher, stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (isbn, title, author, release, genre, description, price, age_recommendation, publisher, stock))

generate_books(100)
cursor.commit()
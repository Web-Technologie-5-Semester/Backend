# requirements
- pipenv 
- fastAPI  
- python 3.12

1. create a virtual environment
- install pip (package installer for python)
- install pipenv: https://pipenv.pypa.io/en/latest/installation.html

2. Install fastAPI
- Installation in your virtual environemten (pipenv install ...)
    https://fastapi.tiangolo.com/tutorial/#run-the-code

3. Database
- create in docker postgres container
- create new database 

4. start fastAPI
- fastapi dev main.py

5. Migrations
erstellen: pipenv run alembic revision --autogenerate -m "Beschreibung der Migration"
anwenden: pipenv run alembic upgrade head

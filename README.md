# requirements
1. Download all these Programms

- python 3.12.7
- Docker
- pgAdmin 4 ()
- Microsoft Build Tools für C++  "https://visualstudio.microsoft.com/de/visual-cpp-build-tools/"


2. Create a virtual environment for the python Project   (venv is recommended with python debugger)
	- install all required packages found in the files (open each file and "pip install" each package you see)
	- install also psycopg2 and exchange jwt for PYjwt
		pip install psycopg2
		pip uninstall jwt
		pip install PYjwt


3. Inside Docker:
	- pull the official image for postgres:alpine
	- Set as the following
		- Container name = db
		- Host Port = 5431
		- Environment variables
			- POSTGRESS_PASSWORD = admin
	
	- everything not explicitly mentioned ist supposed to be default

4. Run the created Docker Image, if not by default also run the now created container  --> Leave them running


5. Open pgAdmin 4
	- Rightclick on Servers   -->   Register Server   -->   General: Name = "webshop"   -->  Connection: Host name/address = "localhost"
												 Connection: Port = "5431"
												 Connection: Password = "admin"
												 
	- everything else is supposed to be left on default

	- Open the Dropdown  -->  Rightclick on your created Server  -->  Create --> Database --> General: Name = "db"
	- everything else is supposed to left on default

	- If everything was set up correctly:
		- open the dropdown of your server(webshop)   -->  open dropdown of you database(db)  -->  open dropdown of "Schemas  -->  open dropdown of "Tables"  --> it´s empty for now....

6. Go back to the python project
	- Under   Backend you will find  "main.py"
	- At the bottom you will find the   __name__=="__main__"   with the port where you can access, via swagger ui (localhost/docs), the different Endpoints in the project (while running)	-->  or use:   http://localhost:8080/docs				    		
	- With everything set
		- Docker Container running
		- pgAdmin to check on your creation of data in the database
		- http://localhost:8080/docs set in the browser

		- run main.py

	- Now you should see the tables in pgAdmin and the Endpoints ready to test in swagger (after reload)
	- Thats for the BackEnd set and done, now to the FrontEnd

 				- ID: "1" | role: "Customer"
				- ID: "2" | role: "Seller"

7. Thats for the BackEnd set and done, now please read the "ReadMe" of the FrontEnd


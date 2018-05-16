# OC Projet 5: Utilisez les données publiques de l'OpenFoodFacts

### User installation:

#### 1 - Requierements:
To install all of the required dependencies open the command prompt and use pip : `pip install -r requirements.txt`

#### 2 - Authorize access to the database:
Use the command : `GRANT ALL PRIVILEGES ON * . * TO 'yourusername'@'localhost' IDENTIFIED BY 'yourpassword';`

#### 3 - Edit the "config.py" file containing the following code :
`DB_USER = 'yourusername'`
`DB_PW = 'yourpassword'`
`DB_NAME = 'yourdbename' `

#### 4 - Start the program
`python main.py`



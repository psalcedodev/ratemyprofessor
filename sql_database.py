import os
import psycopg2
import psycopg2.extras
import urllib.parse


class SquirrelDB:

    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def createProfessorsTable(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS professors (professor_id SERIAL PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), department VARCHAR(255), directory VARCHAR(255))")
        self.connection.commit()

    def createRatingsTable(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS ratings (rating_id SERIAL PRIMARY KEY, rating INTEGER, difficulty INTEGER , retake TEXT, textbook TEXT, attendance TEXT, grade TEXT, comment TEXT, professor_id INTEGER references professors(professor_id))")
        self.connection.commit()

    def createUsersTable(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, f_name VARCHAR(255), l_name VARCHAR(255), email VARCHAR(255), passwd VARCHAR(255))")
        self.connection.commit()

    def insertProfessor(self, first_name, last_name, department, directory):
        data = [first_name, last_name, department, directory]
        self.cursor.execute(
            "INSERT INTO professors (first_name, last_name, department, directory) VALUES (%s, %s, %s, %s)", data)
        self.connection.commit()
    # Inserts a rating for each professor by copying the exact professor's id

    def insertRating(self, course, rating, difficulty, retake, textbook, attendance, grade, comment, professor_id):
        data = [course, rating, difficulty, retake, textbook,
                attendance, grade, comment, professor_id]
        self.cursor.execute(
            "INSERT INTO ratings (course, rating, difficulty, retake, textbook, attendance, grade, comment, professor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", data)
        self.connection.commit()
    # Gets professor's information

    def getProfessors(self):
        self.cursor.execute(
            "SELECT * FROM professors")
        result = self.cursor.fetchall()
        return result

    # Get Ratings
    def getRatings(self):
        self.cursor.execute(
            "SELECT * FROM ratings")
        result = self.cursor.fetchall()
        return result
    # Gets information of only 1 professor

    def getAvg(self, rating_id):
        avg = [rating_id]
        self.cursor.execute(
            "SELECT AVG(rating) as rating FROM ratings WHERE professor_id = %s", avg)
        result = self.cursor.fetchone()
        return result

    def getDifficulty(self, difficulty_id):
        difficulty = [difficulty_id]
        self.cursor.execute(
            "SELECT AVG(difficulty) as difficulty FROM ratings WHERE professor_id = %s", difficulty)
        result = self.cursor.fetchone()
        return result

    def getOneProfessor(self, professor_id):
        data = [professor_id]
        self.cursor.execute(
            "SELECT * FROM professors WHERE professor_id = %s", data)
        # Fetchs from 0 to one item
        result = self.cursor.fetchone()
        return result

    def getOneRating(self, rating_id):
        data = [rating_id]
        self.cursor.execute(
            "SELECT * FROM ratings WHERE professor_id = %s", data)
        result = self.cursor.fetchall()
        return result
    # Deletes a professor and it's comments by it's ID

    def DeleteProfessor(self, delete_id):
        data = [delete_id]
        self.cursor.execute(
            "DELETE FROM professors WHERE professor_id = %s", data)
        self.connection.commit()
        return True

    def DeleteRating(self, delete_id):
        data = [delete_id]
        self.cursor.execute(
            "DELETE FROM ratings WHERE professor_id = %s", data)
        self.connection.commit()
        return True

    def UpdateProfessor(self, f_name, l_name, dept, direct, prof_id):
        data = [f_name, l_name, dept, direct, prof_id]
        self.cursor.execute(
            "UPDATE professors SET first_name = %s, last_name = %s, department = %s, directory = %s WHERE professor_id = %s", data)
        self.connection.commit()
        return True

    def CreateUser(self, f_name, l_name, email, passwd):
        data = [f_name, l_name, email, passwd]
        self.cursor.execute(
            "INSERT INTO users (f_name, l_name, email, passwd) VALUES (%s, %s, %s, %s)", data)
        self.connection.commit()

    def CreateSession(self, email, password):
        data = [email, password]
        self.cursor.execute(
            "INSERT INTO sessions (email, passwd) VALUES (%s, %s)", data)
        self.connection.commit()

    def EmailExist(self, email):
        data = [email]
        self.cursor.execute(
            "SELECT * FROM users WHERE email =%s", data)
        result = self.cursor.fetchone()
        return result

    def login(self, email):
        data = [email]
        self.cursor.execute(
            "SELECT * FROM users WHERE email = %s", data)
        result = self.cursor.fetchone()
        return result

# Import the folowwing classes
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
from sql_database import professorsDB
from urllib.parse import parse_qs
from http import cookies
from passlib.hash import bcrypt
from session_store import SessionStore

SESSION_STORE = SessionStore()


class MyrequestHandler(BaseHTTPRequestHandler):
    def LoginSession(self):
        if "userId" in self.session:
            return True
        else:
            return False
 # Function for send and end headers

    def end_headers(self):
        self.send_cookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def load_cookie(self):
        if "Cookie" in self.headers:
            print("Cookie")
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def load_session(self):
        self.load_cookie()
        # if session ID is in the cookie
        if "sessionId" in self.cookie:
            print("Session was found")
            sessionId = self.cookie["sessionId"].value
            # if session ID matches in the session store
            # save the session for use later (data memeber)
            self.session = SESSION_STORE.getSession(sessionId)
            # otherwise, if session ID is NOT in the session ste
            if self.session == None:
                sessionId = SESSION_STORE.createSession()
                self.session = SESSION_STORE.getSession(sessionId)
                self.cookie["sessionId"] = sessionId
                print("Cokkie and Session ID identified")

        else:
            sessionId = SESSION_STORE.createSession()
            self.session = SESSION_STORE.getSession(sessionId)
            self.cookie["sessionId"] = sessionId
        print("current session:", self.session)
    # Retains all the header methods to be used with GET, POST, DELETE

    def do_OPTIONS(self):
        self.load_session()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    # Gets information

    def do_GET(self):
        self.load_session()
        if self.path == "/professors":
            self.GetProfessors()
        elif self.path == "/ratings":
            self.GetRatings()
        elif self.path.startswith("/professors"):
            self.GetOneProfessor()
        elif self.path.startswith("/ratings"):
            self.GetOneRating()
        elif self.path.startswith("/professor/rating/avg"):
            self.GetAvg()
        elif self.path.startswith("/professor/rating/difficulty"):
            self.GetDifficulty()
        # elif self.path == "/sessions":
        #     self.sessionLogged()
        else:
            self.Handle_Not_Found()

    # Deletes function

    def do_DELETE(self):
        self.load_session()
        if self.path.startswith("/professors"):
            if self.LoginSession():
                self.DeleteProfessor()
            else:
                self.handle401()
        else:
            self.Handle_Not_Found()

    # Update function
    def do_PUT(self):
        self.load_session()
        if self.path.startswith("/professors/"):
            if self.LoginSession():
                self.UpdateProfessor()
            else:
                self.handle401()
        else:
            self.Handle_Not_Found()

    # Create Function
    def do_POST(self):
        self.load_session()
        if self.path == "/professors":
            if self.LoginSession():
                self.AddProfessor()
            else:
                self.handle401()
        elif self.path.startswith("/ratings"):
            if self.LoginSession():
                self.AddRating()
            else:
                self.handle401()
        elif self.path == "/users":
            self.PostUsers()
        elif self.path == "/sessions":
            self.login()
        else:
            self.Handle_Not_Found()

    def Handle_Not_Found(self):
        self.send_error(404)
        self.end_headers()

    def handle401(self):
        self.send_error(401)
        self.end_headers()
################################################################
# __________                   __________
# ___  ____/___  ________________  /___(_)____________________
# __  /_   _  / / /_  __ \  ___/  __/_  /_  __ \_  __ \_  ___/
# _  __/   / /_/ /_  / / / /__ / /_ _  / / /_/ /  / / /(__  )
# /_/      \__,_/ /_/ /_/\___/ \__/ /_/  \____//_/ /_//____/
################################################################

    def GetProfessors(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")

        self.end_headers()
        db = professorsDB()
        professors = db.getProfessors()
        self.wfile.write(bytes(json.dumps(professors), "utf-8"))

    def GetOneProfessor(self):
        parts = self.path.split("/")
        professor_id = parts[2]
        db = professorsDB()
        professor = db.getOneProfessor(professor_id)
        if professor != None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")

            self.end_headers()
            self.wfile.write(bytes(json.dumps(professor), "utf-8"))
        else:
            self.Handle_Not_Found()

    def GetRatings(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        db = professorsDB()
        professors = db.getRatings()
        self.wfile.write(bytes(json.dumps(professors), "utf-8"))

    def GetOneRating(self):
        parts = self.path.split("/")
        professor_id = parts[2]
        db = professorsDB()
        professor = db.getOneRating(professor_id)
        if professor != None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(professor), "utf-8"))
        else:
            self.Handle_Not_Found()

    def GetAvg(self):
        parts = self.path.split("/")
        professor_id = parts[-1]
        db = professorsDB()
        professor = db.getAvg(professor_id)
        if professor != None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")

            self.end_headers()
            self.wfile.write(bytes(json.dumps(professor), "utf-8"))
        else:
            self.Handle_Not_Found

    def GetDifficulty(self):
        parts = self.path.split("/")
        professor_id = parts[-1]
        db = professorsDB()
        professor = db.getDifficulty(professor_id)
        if professor != None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")

            self.end_headers()
            self.wfile.write(bytes(json.dumps(professor), "utf-8"))
        else:
            self.Handle_Not_Found()

    # Updates a Professor's information
    def UpdateProfessor(self):
        if not self.LoginSession():
            self.handle401()
            return

        parts = self.path.split("/")
        professor_id = parts[2]
        db_update = professorsDB()
        professor = db_update.getOneProfessor(professor_id)
        if professor != None:
            lenght = self.headers["Content-Length"]
            # read the body
            body = self.rfile.read(int(lenght)).decode("utf-8")
            # parse the body
            parsed_body = parse_qs(body)
            f_name = parsed_body["f_name"][0]
            l_name = parsed_body["l_name"][0]
            dept = parsed_body["dept"][0]
            direct = parsed_body["direct"][0]
            prof_id = professor_id
            db_update.UpdateProfessor(
                f_name, l_name, dept, direct, prof_id)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")

            self.end_headers()
        else:
            self.Handle_Not_Found()

    def DeleteProfessor(self):
        parts = self.path.split("/")
        delete_id = parts[2]
        db = professorsDB()
        professor = db.getOneProfessor(delete_id)
        if professor != None:

            db.DeleteProfessor(delete_id)
            db.DeleteRating(delete_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")

            self.end_headers()
            self.wfile.write(bytes(json.dumps(professor), "utf-8"))
        else:
            self.Handle_Not_Found()

    def AddProfessor(self):
        # 1. unpack the body(data)
        lenght = self.headers["Content-Length"]
        # read the body
        body = self.rfile.read(int(lenght)).decode("utf-8")
        # parse the body
        parsed_body = parse_qs(body)
        # Save professor's info
        first_name = parsed_body["first_name"][0]
        last_name = parsed_body["last_name"][0]
        department = parsed_body["department"][0]
        directory = parsed_body["directory"][0]
        db_post = professorsDB()
        db_post.insertProfessor(
            first_name, last_name, department, directory)
        # Print
        # 2. respond to the client
        self.send_response(201)
        self.send_header("Content-Type", "application/json")

        self.end_headers()

    def AddRating(self):
        parts = self.path.split("/")
        professor_id = parts[-1]
        lenght = self.headers["Content-Length"]
        # read the body
        body = self.rfile.read(int(lenght)).decode("utf-8")
        # parse the body
        parsed_body = parse_qs(body)
        course = parsed_body["course"][0]
        rating = parsed_body["rating"][0]
        difficulty = parsed_body["difficulty"][0]
        retake = parsed_body["retake"][0]
        textbook = parsed_body["textbook"][0]
        attendance = parsed_body["attendance"][0]
        grade = parsed_body["grade"][0]
        comment = parsed_body["comment"][0]
        profid = professor_id
        db_update = professorsDB()
        db_update.insertRating(
            course, rating, difficulty, retake, textbook, attendance, grade, comment, profid)

        self.send_response(201)
        self.send_header("Content-Type", "application/json")

        self.end_headers()

    def PostUsers(self):
        db = professorsDB()
        # 1. unpack the body(data)
        lenght = self.headers["Content-Length"]
        # read the body
        body = self.rfile.read(int(lenght)).decode("utf-8")
        # parse the body
        parsed_body = parse_qs(body)
        # Save professor's info
        firstName = parsed_body["firstName"][0]
        lastName = parsed_body["lastName"][0]
        email = parsed_body["email"][0]
        passwd = parsed_body["passwd"][0]
        user = db.login(email)

        if user != None:
            self.send_response(422)
            self.end_headers()
        else:
            hashpwd = bcrypt.hash(passwd)
            db.CreateUser(firstName, lastName,
                          email, hashpwd)
            # self.session['userId'] = user['id']
            # 2. respond to the client
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

    def login(self):
        lenght = self.headers["Content-Length"]
        body = self.rfile.read(int(lenght)).decode("utf-8")
        # parse the body
        parsed_body = parse_qs(body)
        # Save professor's info
        email = parsed_body["email"][0]
        passwd = parsed_body["passwd"][0]

        db = professorsDB()
        user = db.login(email)
        if user != None:
            if bcrypt.verify(passwd, user["passwd"]):

                self.session['userId'] = user['id']
                self.send_response(201)
                self.send_header("Content-Type", "application/json")

                self.end_headers()
                print("User logged as: " + email)
            else:
                self.handle401()
        else:
            self.handle401()


def run():
    db = professorsDB()
    db.createProfessorsTable()
    db.createRatingsTable()
    db.createUsersTable()
    db = None  # disconnect

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)
    server = HTTPServer(listen, MyrequestHandler)

    print("Server listening on", "{}:{}".format(*listen))
    server.serve_forever()


run()
